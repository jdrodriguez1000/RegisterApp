from models.dashboard_model import DashboardModel
from core.database import supabase
from core.logger import get_logger
from core.state import AppState
from core.i18n import I18n

logger = get_logger(__name__)

class DashboardController:
    def __init__(self, model: DashboardModel):
        self.model = model

    def load_user_data(self):
        """
        Fetches user data, using AppState cache if available.
        """
        self.model.is_loading = True
        
        try:
            # 1. OPTIMIZATION: Check Global Cache first
            if AppState.is_cache_valid():
                logger.info("Using cached user data for Dashboard")
                user = AppState.get_user_cache()
                profile = AppState.get_profile_cache()
                self._map_to_model(user, profile)
                self.model.is_loading = False
                return True

            # 2. Cache miss: Fetch from Remote
            logger.info("Cache miss. Fetching from Supabase...")
            user_response = supabase.auth.get_user()
            user = user_response.user if user_response else None
            
            if not user:
                self.model.error_message = "No hay sesión activa"
                self.model.is_loading = False
                return False
            
            # Fetch profile
            profile_response = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            profile = profile_response.data if profile_response else None
            
            # 3. Update Global Cache
            AppState.set_user_cache(user, profile)
            
            # 4. Map to Model
            self._map_to_model(user, profile)
            
            self.model.is_loading = False
            return True
            
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")
            self.model.error_message = f"Error al cargar datos: {str(e)}"
            self.model.is_loading = False
            return False

    def _map_to_model(self, user, profile):
        """Helper to map cached/remote data to the model."""
        # Basic Auth Data
        self.model.email = user.email or ""
        self.model.full_name = user.user_metadata.get("full_name", "Usuario")
        
        # Profile Data
        if profile:
            self.model.gender = I18n.get_list_item("lists.genders", profile.get("gender")) or I18n.t("dashboard.not_specified")
            self.model.birth_date = profile.get("birth_date") or ""
            self.model.civil_status = I18n.get_list_item("lists.civil_statuses", profile.get("civil_status")) or ""
            self.model.favorite_color = I18n.get_list_item("lists.colors", profile.get("favorite_color")) or ""
            self.model.favorite_sport = I18n.get_list_item("lists.sports", profile.get("favorite_sport")) or ""
