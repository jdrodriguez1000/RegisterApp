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
        if not self.email:
            return "El correo es obligatorio"
        if "@" not in self.email:
            return "Ingresa un correo válido"
        if not self.password:
            return "La contraseña es obligatoria"
        # Removed "Password too short" check for login, just check empty. Supabase will check validity.
        return None
