from core.state import AppState

class LoginModel:
    """
    Model for handling login data and state
    """
    def __init__(self):
        self.email = ""
        self.password = ""
        self.is_loading = False
        self.error_message = None

    def validate(self):
        if not self.email or "@" not in self.email:
            return "Invalid email"
        if not self.password or len(self.password) < 6:
            return "Password too short"
        return None
