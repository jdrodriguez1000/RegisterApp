from core.security import is_password_strong, get_password_strength_message_key

class ChangePasswordModel:
    def __init__(self):
        self.current_password = ""
        self.new_password = ""
        self.confirm_password = ""
        self.error_message = ""
        self.is_loading = False

    def validate(self):
        """Validates the password change fields."""
        if not self.current_password or not self.new_password or not self.confirm_password:
            return "register.error_empty"
        
        if self.new_password != self.confirm_password:
            return "change_password.error_mismatch"
            
        if self.new_password == self.current_password:
            return "change_password.error_same_as_old"
            
        strength_error = get_password_strength_message_key(self.new_password)
        if strength_error:
            return strength_error
            
        return None
