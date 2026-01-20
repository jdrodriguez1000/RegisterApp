from models.user_profile import UserProfile
from core.database import supabase
from core.logger import get_logger
from core.state import AppState
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
            # 1. OPTIMIZATION: Check Global Cache
            if AppState.is_cache_valid():
                logger.info("Using cached profile data")
                user = AppState.get_user_cache()
                profile = AppState.get_profile_cache()
                self._map_to_model(user, profile)
                return True

            # 2. Remote Fetch
            user_response = supabase.auth.get_user()
            user = user_response.user if user_response else None
            if not user:
                return False
            
            profile_response = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            profile = profile_response.data if profile_response else None
            
            # 3. Cache it
            AppState.set_user_cache(user, profile)
            
            # 4. Map
            self._map_to_model(user, profile)
            return True

        except Exception as e:
            logger.error(f"Error fetching profile: {str(e)}")
            return False
        finally:
            self.is_loading = False

    def _map_to_model(self, user, profile):
        """Helper to map session data to Profile model."""
        # Auth data for display
        self.model.email = user.email
        self.model.full_name = user.user_metadata.get("full_name", "Usuario")
        
        # Profile table data
        if profile:
            self.model.gender = profile.get("gender")
            self.model.civil_status = profile.get("civil_status")
            self.model.favorite_color = profile.get("favorite_color")
            self.model.favorite_sport = profile.get("favorite_sport")
            
            # Parse date
            bdate = profile.get("birth_date")
            if bdate:
                try:
                    self.model.birth_date = datetime.strptime(bdate, "%Y-%m-%d")
                except:
                    self.model.birth_date = None

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
            
            # 5. ATOMIC CACHE UPDATE
            # Only update the cache if the DB operation succeeded
            AppState.update_profile_cache(data)
            
            logger.info("Profile and Cache updated successfully")
            return True

        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            self.error_message = f"Error al guardar el perfil: {str(e)}"
            self.is_loading = False
            page.update()
            return False
