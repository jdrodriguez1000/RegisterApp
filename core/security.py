import re

def is_password_strong(password: str) -> bool:
    """
    Checks if a password is strong.
    Criteria:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>+_-]', password):
        return False
    return True

def get_password_strength_message_key(password: str) -> str:
    """
    Returns a translation key describing why a password is weak.
    """
    if len(password) < 8:
        return "security.password_too_short"
    if not re.search(r'[A-Z]', password):
        return "security.password_no_upper"
    if not re.search(r'[a-z]', password):
        return "security.password_no_lower"
    if not re.search(r'\d', password):
        return "security.password_no_digit"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>+_-]', password):
        return "security.password_no_special"
    return None
