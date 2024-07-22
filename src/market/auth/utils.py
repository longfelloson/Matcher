import jwt
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users.models import User
from database import get_async_session
from market.auth.token import decode_token
from bot.users import crud as users_crud


class AuthGuard:
    async def __call__(self, request: Request):
        if not (token := request.cookies.get("token")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            if decode_token(token):
                return True
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_current_user(request: Request, session: AsyncSession = Depends(get_async_session)) -> User:
    """
    Gets current user and returns it
    """
    payload = decode_token(request.cookies.get("token"))
    return await users_crud.get_user(payload['sub'], session)


auth_guard = AuthGuard()
