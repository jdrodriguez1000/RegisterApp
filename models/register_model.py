from core.database import supabase

class RegisterModel:
    def __init__(self):
        self.full_name = ""
        self.email = ""
        self.password = ""
        self.error_message = ""
        self.is_loading = False

    def validate(self):
        """Validates the registration fields (No Vacíos and Basic Security)."""
        if not self.full_name or not self.email or not self.password:
            return "register.error_empty"
        
        if "@" not in self.email or "." not in self.email:
            return "register.error_email"
            
        if len(self.password) < 6:
            return "register.error_password"
            
        return None
