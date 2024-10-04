from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users.guesses.states import GuessesState
from bot.users.guesses.utils import react_for_user_guess
from bot.users.models import User
from bot.users.utils import get_user_for_view

router = Router(name="Guesses")


@router.message(GuessesState.user_age, F.text.isdigit())
async def age_guess_button_handler(
        message: Message,
        session: AsyncSession,
        state: FSMContext,
        user: User,
):
    """Обработка кнопок угадывания возрасты анкеты"""
    user_for_view = await get_user_for_view(state, session)

    await react_for_user_guess(message, user, session, user_for_view, state)
