from datetime import (
    datetime,
    timedelta,
    timezone,
)
from typing import Optional
from fastapi import HTTPException, status
import jwt

from config import settings


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            detail={"Token expried"}, status_code=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            detail={"Invalid token"}, status_code=status.HTTP_401_UNAUTHORIZED
        )
