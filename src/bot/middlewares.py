from typing import Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from bot.users import crud as users_crud
from bot.users.enums import UserStatus
from database import get_async_session


class PayloadMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, update: Update, data: Dict):
        """
        "Прослойка", возвращающая полезную нагрузку для обработчиков (хендлеров)
        """
        message = update.callback_query if update.callback_query else update.message
        async for session in get_async_session():
            data["session"] = session
            data["user"] = await users_crud.get_user(message.from_user.id, session)
            data["data"] = {}
            return await handler(update, data)


class BlockedUserMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, message: Message, data: dict):
        """
        "Прослойка" для заблокированных пользователей
        """
        user_id = message.chat.id
        user = await users_crud.get_user(user_id, data["session"])
        if not user or user.status != UserStatus.blocked:
            return await handler(message, data)
        await message.answer("Вы заблокированы в боте ⛔️")
