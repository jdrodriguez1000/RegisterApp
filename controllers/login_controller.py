from models.login_model import LoginModel
from core.logger import get_logger

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
            # Placeholder for Supabase Auth call
            logger.info(f"Attempting login for: {email}")
            # router.navigate("/dashboard")
            return True
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            self.model.error_message = "Authentication failed"
            self.model.is_loading = False
            return False
