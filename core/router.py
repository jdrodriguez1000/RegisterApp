import flet as ft
from core.logger import get_logger
from core.database import supabase
from core.state import AppState

logger = get_logger("Router")

class Router:
    def __init__(self, page):
        self.page = page
        self.current_route = "/"
        self.routes = self._load_routes()

    def _load_routes(self):
        from configs.routes import routes
        return routes

    def navigate(self, route):
        """
        Safe navigation with business logic shielding.
        """
        # 1. Apply Navigation Shielding (Security & Logic flow)
        target_route = self._shield_route(route)
        
        # 2. Check if route exists
        if target_route not in self.routes:
            logger.warning(f"Route not found: {target_route}")
            target_route = "/"

        # 3. Avoid redundant navigation
        if target_route == self.current_route and len(self.page.controls) > 0:
            return

        logger.info(f"Navigating to: {target_route} (Requested: {route})")
        
        self.current_route = target_route
        self.page.controls.clear()

        try:
            # Build and render the view
            view = self.routes[target_route](self.page, self)
            self.page.add(view)
        except Exception as e:
            logger.exception(f"Error rendering view: {target_route}")
            # Fallback to a safe place or error handler
            self.page.add(ft.Text(f"Internal Error: {str(e)}", color="red"))

        self.page.update()

    def _shield_route(self, route):
        """
        Intercepts navigation attempts and enforces mandatory business flows.
        Returns the safe target route.
        """
        # 1. Technical Session Check
        try:
            # Note: supabase.auth.get_user() is relatively fast as it checks local session first
            user_response = supabase.auth.get_user()
            user = user_response.user if user_response else None
        except:
            user = None

        # 2. Public exceptions (Allowed if NOT authenticated)
        # If authenticated, "/" should go to dashboard for better UX
        if route in ["/construction"]:
            return route
        
        if route == "/":
            if not user:
                return route
            # If user exists, fall through to profile check logic

        # 3. SHIELD: Unauthenticated Users
        if not user:
            # Can only access Auth pages or Welcome
            if route in ["/login", "/register"]:
                return route
            return "/login"

        # 4. SHIELD: Email Verification (If mandatory)
        # Note: In some workflows you might want to bypass this for local testing
        # user.email_confirmed_at is standard in Supabase
        if hasattr(user, 'email_confirmed_at') and user.email_confirmed_at is None:
            if route == "/verification-pending":
                return route
            return "/verification-pending"

        # 5. SHIELD: Profile Completion (Phase 5/7 requirement)
        profile = None
        if AppState.is_cache_valid():
            profile = AppState.get_profile_cache()
        else:
            # Fetch minimal data to decide flow
            try:
                profile_res = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
                profile = profile_res.data
                AppState.set_user_cache(user, profile)
            except:
                pass # Profile might not exist yet if register trigger fails

        required_fields = ["gender", "birth_date", "civil_status", "favorite_color", "favorite_sport"]
        is_complete = profile and all(profile.get(f) for f in required_fields)

        if not is_complete:
            if route == "/profile-completion":
                return route
            return "/profile-completion"

        # 6. SHIELD: Logged in users shouldn't go back to login/register or welcome
        if route in ["/", "/login", "/register", "/profile-completion", "/verification-pending"]:
            return "/dashboard"

        return route
