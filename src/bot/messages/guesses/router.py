from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.messages.commands.enums import CommandAnswer
from bot.messages.guesses.keyboards import ALL_AGE_GROUPS
from bot.messages.guesses.states import GuessesStates
from bot.messages.guesses.utils import react_for_user_guess
from bot.users.models import User
from bot.users.utils import get_user_for_view

router = Router(name="Guesses")


@router.message(GuessesStates.user_age, F.text.in_(ALL_AGE_GROUPS))
async def age_guess_button_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    """Обработка кнопок угадывания возрасты анкеты"""
    user_for_view = await get_user_for_view(state, session)

    await react_for_user_guess(message, user, session, user_for_view, state)


@router.message(GuessesStates.user_age, F.text == "↩")
async def back_button_handler(message: Message):
    """Обработка кнопки 'Назад' в состоянии угадывания возраста"""
    await message.answer(CommandAnswer.start, reply_markup=main_keyboard())
