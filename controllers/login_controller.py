from models.login_model import LoginModel
from core.logger import get_logger
from core.database import supabase # Ensure this export exists in core/database.py

logger = get_logger("LoginController")

class LoginController:
    """
    Controller for login page logic
    """
    def __init__(self, model=None):
        self.model = model or LoginModel()

    async def handle_login(self, email, password, page, router):
        self.model.email = email
        self.model.password = password
        self.model.is_loading = True
        self.model.error_message = None
        
        validation_error = self.model.validate()
        if validation_error:
            self.model.error_message = validation_error
            self.model.is_loading = False
            return False

        try:
            logger.info(f"Attempting login for: {email}")
            
            # Real Supabase Authentication
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            # If successful, response.user and response.session should be populated
            if response.user:
                logger.info(f"Login successful for user: {response.user.id}")
                return True
            else:
                self.model.error_message = "No user returned from authentication."
                return False

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            # Improve error message handling based on Supabase exceptions if possible
            if "Invalid login credentials" in str(e):
                self.model.error_message = "Credenciales incorrectas"
            else:
                self.model.error_message = f"Error: {str(e)}"
            self.model.is_loading = False
            return False
