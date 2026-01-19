from models.user_profile import UserProfile
from core.database import supabase
from core.logger import get_logger

logger = get_logger("ProfileController")

class ProfileController:
    def __init__(self, model=None):
        self.model = model or UserProfile()
        self.error_message = None
        self.is_loading = False

    async def save_profile(self, page, router):
        self.is_loading = True
        page.update()
        
        error = self.model.validate()
        if error:
            self.error_message = error
            self.is_loading = False
            page.update()
            return False

        try:
            user = supabase.auth.get_user()
            if not user or not user.user:
                raise Exception("No user logged in")

            user_id = user.user.id
            
            # Format date for Supabase (YYYY-MM-DD)
            birth_date_str = self.model.birth_date.strftime("%Y-%m-%d") if self.model.birth_date else None

            data = {
                "gender": self.model.gender,
                "birth_date": birth_date_str,
                "civil_status": self.model.civil_status,
                "favorite_color": self.model.favorite_color,
                "favorite_sport": self.model.favorite_sport,
                "updated_at": "now()"
            }

            logger.info(f"Updating profile for user {user_id}: {data}")

            # Update profile in Supabase
            response = supabase.table("profiles").update(data).eq("id", user_id).execute()
            
            # Check if successful (Supabase-py usually raises error or returns data)
            # If we are here, it likely succeeded.
            
            logger.info("Profile updated successfully")
            
            # Navigate to Construction Page as per Phase 5 instructions (Dashboard is next phase)
            router.navigate("/construction")
            return True

        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            self.error_message = f"Error al guardar el perfil: {str(e)}"
            self.is_loading = False
            page.update()
            return False
