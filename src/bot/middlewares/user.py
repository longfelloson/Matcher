from typing import Callable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.keyboards import help_command_keyboard
from bot.users import crud as users_crud
from bot.users.enums.answers import WarningAnswer
from bot.users.enums.statuses import UserStatus


class UserStatusMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable,
            event: Union[Message, CallbackQuery],
            data: dict,
    ):
        """'Прослойка' для проверки статуса пользователя"""
        event_message = event if isinstance(event, Message) else event.message

        user_id = event_message.chat.id
        user = await users_crud.get_user(user_id, data["session"])

        session = data["session"]

        if not user:
            return await handler(event, data)

        if user.status == UserStatus.blocked:
            return await event_message.answer(WarningAnswer.blocked_user, reply_markup=help_command_keyboard())
        elif user.status == UserStatus.left:
            await users_crud.update_user(user.user_id, session, status=UserStatus.active)

        return await handler(event, data)
