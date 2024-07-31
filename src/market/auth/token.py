from datetime import timedelta, timezone, datetime
from typing import Optional

import jwt

from config import settings


def get_auth_link(user_id: int) -> str:
    """
    Получает ссылку для авторизации по JWT-токену в параметре
    """
    token = create_access_token({"sub": user_id})
    return f"/auth?token={token}"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH.JWT_SECRET_KEY, algorithm=settings.AUTH.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    return jwt.decode(
        token, settings.AUTH.SECRET_KEY, algorithms=settings.AUTH.ALGORITHM
    )
