from models.dashboard_model import DashboardModel
from core.database import supabase
from core.logger import get_logger

logger = get_logger(__name__)

class DashboardController:
    def __init__(self, model: DashboardModel):
        self.model = model

    def load_user_data(self):
        """
        Fetches user data from Supabase Auth and Profiles table.
        """
        self.model.is_loading = True
        try:
            # 1. Get Current User/Session
            # Note: get_user() retrieves user from local session storage if available
            user = supabase.auth.get_user().user
            
            if not user:
                self.model.error_message = "No hay sesión activa"
                self.model.is_loading = False
                return False
            
            # 2. Get Basic Info from Metadata
            self.model.email = user.email or ""
            # Meta data is usually in user_metadata dict
            self.model.full_name = user.user_metadata.get("full_name", "Usuario")
            
            # 3. Get Extended Info from Profiles Table
            response = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            
            from core.i18n import I18n
            if response.data:
                p = response.data
                self.model.gender = I18n.get_list_item("lists.genders", p.get("gender")) or I18n.t("dashboard.not_specified")
                # Format birth date if needed, assuming ISO string YYYY-MM-DD
                self.model.birth_date = p.get("birth_date") or ""
                self.model.civil_status = I18n.get_list_item("lists.civil_statuses", p.get("civil_status")) or ""
                self.model.favorite_color = I18n.get_list_item("lists.colors", p.get("favorite_color")) or ""
                self.model.favorite_sport = I18n.get_list_item("lists.sports", p.get("favorite_sport")) or ""
                
            self.model.is_loading = False
            return True
            
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")
            self.model.error_message = f"Error al cargar datos: {str(e)}"
            self.model.is_loading = False
            return False
