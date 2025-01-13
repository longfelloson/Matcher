from typing import Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.users import crud as users_crud
from database import get_async_session


class PayloadMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, update: Update, data: Dict):
        message = update.callback_query if update.callback_query else update.message
        async for session in get_async_session():
            data["session"] = session
            data["user"] = await users_crud.get_user_by_id(
                message.from_user.id, session
            )
            data["data"] = {}
            return await handler(update, data)
