import os
import re

from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext


# Configuración para proteger las contraseñas
password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Configuración del token JWT
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "actividad4-clave-desarrollo"
)

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    """Convierte una contraseña normal en un hash."""
    return password_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """Comprueba si una contraseña coincide con su hash."""
    return password_context.verify(
        plain_password,
        hashed_password
    )


def validate_email(email: str) -> bool:
    """Valida el formato básico de un correo electrónico."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def create_access_token(
    user_id: int,
    email: str
) -> str:
    """Genera un token JWT para un usuario autenticado."""

    expiration = (
        datetime.now(timezone.utc)
        + timedelta(minutes=JWT_EXPIRE_MINUTES)
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expiration
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )