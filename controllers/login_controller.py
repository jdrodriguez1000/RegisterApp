from models.login_model import LoginModel
from core.logger import get_logger
from core.database import supabase

logger = get_logger("LoginController")

class LoginController:
    """
    Controller for login page logic
    """
    def __init__(self, model=None):
        self.model = model or LoginModel()

    async def handle_login(self, email, password, page, router):
        """
        Handles login and determines the next route based on profile completion.
        Returns the route string if successful, None otherwise.
        """
        self.model.email = email
        self.model.password = password
        self.model.is_loading = True
        self.model.error_message = None
        
        validation_error = self.model.validate()
        if validation_error:
            self.model.error_message = validation_error
            self.model.is_loading = False
            return None

        try:
            logger.info(f"Attempting login for: {email}")
            
            # 1. Supabase Authentication
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            user = response.user
            if user:
                logger.info(f"Login successful for user: {user.id}")
                
                # 2. Check Profile Completion
                # Fetch profile fields to check if they are populated
                profile_response = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
                
                profile = profile_response.data
                
                if not profile:
                    # Should unlikely happen if trigger works, but safe fallback
                    logger.warning("No profile found for user, redirecting to completion")
                    return "/profile-completion"
                
                # Check for mandatory fields (Phase 5 fields)
                # full_name is from Phase 4, so we check Phase 5 spec
                required_fields = ["gender", "birth_date", "civil_status", "favorite_color", "favorite_sport"]
                
                is_complete = all(profile.get(field) for field in required_fields)
                
                if not is_complete:
                    logger.info("Profile incomplete. Redirecting to completion.")
                    return "/profile-completion"
                else:
                    logger.info("Profile complete. Redirecting to Dashboard.")
                    return "/dashboard"
            else:
                self.model.error_message = "No user returned from authentication."
                return None

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            if "Invalid login credentials" in str(e):
                self.model.error_message = "Credenciales incorrectas"
            else:
                self.model.error_message = f"Error: {str(e)}"
            self.model.is_loading = False
            return None
