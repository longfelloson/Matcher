from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.messages.guesses.keyboards import ALL_GROUPS_AGES
from bot.messages.guesses.states import GuessesStates
from bot.messages.guesses.utils import react_for_user_guess
from bot.messages.schemas import Answers
from bot.users.models import User

router = Router(name="Guesses")


@router.message(GuessesStates.guess_user_age, F.text.in_(ALL_GROUPS_AGES))
async def age_guess_button_handler(message: Message, session: AsyncSession, state: FSMContext, user: User):
    """
    Обработка кнопок угадывания возрасты анкеты
    """
    await react_for_user_guess(message, user, session, state)
    # await send_photo(message, user, session, state)


@router.message(GuessesStates.guess_user_age, F.text == "↩")
async def back_button_handler(message: Message):
    """
    Обработка кнопки "Назад" в состоянии угадывания возраста
    """
    await message.answer(Answers.GREETING, reply_markup=main_keyboard())
