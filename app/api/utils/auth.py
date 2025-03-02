from datetime import datetime, timedelta, UTC

from jose import jwt
from passlib.hash import bcrypt

from app.core.settings import get_settings

settings = get_settings()


def check_password(hashed_password, password) -> bool:
    return bcrypt.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ENCRYPT_ALGORITHM)
    return encoded_jwt
