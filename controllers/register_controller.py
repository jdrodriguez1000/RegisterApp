from core.database import supabase
import logging

logger = logging.getLogger(__name__)

class RegisterController:
    def __init__(self, model):
        self.model = model

    async def handle_register(self, full_name, email, password, page, router):
        """
        Handles the user registration process using Supabase.
        Ensures 'Identidad Digital' starts with a verified email.
        """
        self.model.full_name = full_name
        self.model.email = email
        self.model.password = password
        
        # 1. No Vacíos & Validation
        error_key = self.model.validate()
        if error_key:
            self.model.error_message = error_key
            return False
            
        self.model.is_loading = True
        self.model.error_message = ""
        page.update()
        
        try:
            # 2. Supabase Auth (Cripta Segura)
            # We include the display name in user metadata for 'Identidad Digital'
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            })
            
            if response.user:
                logger.info(f"Registration successful for: {email}")
                return True
            else:
                self.model.error_message = "Error en el registro"
                return False
                
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            # Handle specific Supabase errors if needed
            self.model.error_message = str(e)
            return False
        finally:
            self.model.is_loading = False
            page.update()
