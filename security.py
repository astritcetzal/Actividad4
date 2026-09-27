from passlib.context import CryptContext
import re


# Configuración para proteger las contraseñas
password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """Convierte una contraseña normal en un hash."""
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Comprueba si una contraseña coincide con su hash."""
    return password_context.verify(
        plain_password,
        hashed_password
    )


def validate_email(email: str) -> bool:
    """Valida el formato básico de un correo electrónico."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None