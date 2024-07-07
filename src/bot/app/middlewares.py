from typing import Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from bot.guesses.states import GuessesStates
from bot.messages.schemas import Answers
from bot.rates.states import RatesStates
from bot.users import crud as users_crud
from bot.users.schemas import UserStatuses
from database import get_async_session


class PayloadMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, update: Update, data: Dict):
        message = update.callback_query if update.callback_query else update.message
        async for session in get_async_session():
            data['session'] = session
            data['user'] = await users_crud.get_user(message.from_user.id, session)
            data['data'] = {}
            return await handler(update, data)


class UserStatusMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, message: Message, data: Dict):
        current_state = await data['state'].get_state()
        user = data.get('user')
        if not user:
            return await handler(message, data)
        elif current_state in [RatesStates.rate_user,
                               GuessesStates.guess_user_age] and user.status == UserStatuses.NOT_REGISTERED:
            ...
        elif user.status == UserStatuses.ACTIVE:
            return await handler(message, data)
        elif user.status == UserStatuses.BLOCKED:
            await message.answer(Answers.BLOCKED_USER)
        return await handler(message, data)
