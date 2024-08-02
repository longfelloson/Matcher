from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages.guesses.keyboards import USER_RATE_BUTTONS
from bot.messages.rates.utils import react_for_user_rate
from bot.users.models import User
from bot.users.utils import send_user_for_view

router = Router(name="Rates")


@router.message(F.text.in_(USER_RATE_BUTTONS))
async def rate_user_button_handler(
        message: Message, session: AsyncSession, state: FSMContext, user: User
):
    """
    Обработка кнопок оценки и угадывания возрасты анкеты
    """
    await react_for_user_rate(message, user, state, session)
    await send_user_for_view(message, user, session, state)
