from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)

from bot.users import crud as users_crud
from bot.users.models import User
from database import SessionWithoutCommit
from market.auth.schemas import User as UserSchema
from market.auth.token import decode_token, create_access_token


def get_auth_link(user_id: int) -> str:
    token = create_access_token({"sub": user_id})
    return f"/auth?token={token}"


async def get_current_user(
    request: Request, session: SessionWithoutCommit,
    ) -> User:
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: Missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await users_crud.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


CurrentUser = Annotated[UserSchema, Depends(get_current_user)]
