import re

def validate_password(password):
    """
    Validate password with the following criteria:
    - At least 6 characters long
    - Must contain at least one letter (a-z, A-Z)
    - Must contain at least one digit (0-9)
    - Must contain at least one special character
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    has_letter = re.search(r'[a-zA-Z]', password)
    has_digit = re.search(r'[0-9]', password)
    has_special = re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password)
    
    if not has_letter:
        return False, "Password must contain at least one letter"
    if not has_digit:
        return False, "Password must contain at least one digit"
    if not has_special:
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"