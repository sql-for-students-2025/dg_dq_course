class ValidationError(Exception):
    """Базовое исключение для ошибок валидации"""
    pass

class EmailValidationError(ValidationError):
    """Ошибка валидации email"""
    pass
    
class PasswordValidationError(ValidationError):
    """Ошибка валидации пароля"""
    pass
    
def validate_email(email):
    """Проверяет валидность email"""
    if not email:
        raise EmailValidationError("Email не может быть пустым")
    if '@' not in email:
        raise EmailValidationError("Email должен содержать @")
    return True

def validate_password(password):
    """Проверяет валидность пароля"""
    if len(password) < 8:
        raise PasswordValidationError("Пароль должен быть не менее 8 символов")
    if not any(char.isdigit() for char in password):
        raise PasswordValidationError("Пароль должен содержать цифру")
    return True

def register_user(email, password):
    """Регистрирует пользователя с валидацией"""
    try:
        validate_email(email)
        validate_password(password)
        print("Регистрация успешна!")
        return True
    except ValidationError as e:
        print(f"Ошибка регистрации: {e}")
    return False

# Использование
register_user("userexample.com", "Strong123") # Успех
register_user("user@example.com", "weak") # Ошибка
register_user("user@example.com", "password") # Ошибка
register_user("user@example.com", "Strong123") # Успех