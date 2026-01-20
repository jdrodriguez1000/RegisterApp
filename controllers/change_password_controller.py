from core.database import supabase
import logging

logger = logging.getLogger(__name__)

class ChangePasswordController:
    def __init__(self, model):
        self.model = model

    async def handle_change_password(self, current_password, new_password, confirm_password, page):
        self.model.current_password = current_password
        self.model.new_password = new_password
        self.model.confirm_password = confirm_password
        
        error_key = self.model.validate()
        if error_key:
            self.model.error_message = error_key
            page.update()
            return False
            
        self.model.is_loading = True
        self.model.error_message = ""
        page.update()
        
        try:
            # 1. Verify current password by attempting to sign in
            # Get current user email first
            user_response = supabase.auth.get_user()
            if not user_response.user:
                self.model.error_message = "session_expired" # You might need this key too
                return False
                
            email = user_response.user.email
            
            try:
                # Re-authenticate to verify current password
                auth_check = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": current_password
                })
            except Exception:
                self.model.error_message = "change_password.error_current_wrong"
                return False

            # 2. Update to new password
            response = supabase.auth.update_user({
                "password": new_password
            })
            
            if response.user:
                logger.info(f"Password updated for: {email}")
                return True
            else:
                self.model.error_message = "Error en la actualización"
                return False
                
        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            self.model.error_message = str(e)
            return False
        finally:
            self.model.is_loading = False
            page.update()
