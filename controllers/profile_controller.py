from models.user_profile import UserProfile
from core.database import supabase
from core.logger import get_logger
from datetime import datetime

logger = get_logger("ProfileController")

class ProfileController:
    def __init__(self, model=None):
        self.model = model or UserProfile()
        self.error_message = None
        self.is_loading = False

    async def get_profile(self):
        self.is_loading = True
        try:
            user_response = supabase.auth.get_user()
            if not user_response or not user_response.user:
                return False
            user_id = user_response.user.id
            response = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
            
            if response.data:
                data = response.data
                self.model.gender = data.get("gender")
                self.model.civil_status = data.get("civil_status")
                self.model.favorite_color = data.get("favorite_color")
                self.model.favorite_sport = data.get("favorite_sport")
                
                # Auth data for display
                self.model.email = user_response.user.email
                self.model.full_name = user_response.user.user_metadata.get("full_name", "Usuario")
                
                # Parse date
                bdate = data.get("birth_date")
                if bdate:
                    self.model.birth_date = datetime.strptime(bdate, "%Y-%m-%d")
                
                return True
        except Exception as e:
            logger.error(f"Error fetching profile: {str(e)}")
            return False
        finally:
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
            supabase.table("profiles").update(data).eq("id", user_id).execute()
            
            logger.info("Profile updated successfully")
            return True

        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            self.error_message = f"Error al guardar el perfil: {str(e)}"
            self.is_loading = False
            page.update()
            return False
