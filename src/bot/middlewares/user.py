from typing import Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.keyboards import help_command_keyboard
from bot.users import crud as users_crud
from bot.users.enums import UserStatus


class BlockedUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        message: Message,
        data: dict,
    ):
        """'Прослойка" для заблокированных пользователей"""
        user_id = message.chat.id
        user = await users_crud.get_user(user_id, data["session"])
        if not user or user.status != UserStatus.blocked:
            return await handler(message, data)
        await message.answer("Вы заблокированы ⛔️", reply_markup=help_command_keyboard())
