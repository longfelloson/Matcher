from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.guesses.keyboards import USER_RATE_BUTTONS
from src.guesses.states import GuessesStates
from src.rates.states import RatesStates
from src.rates.utils import react_for_user_rate
from src.users.models import User
from src.users.utils import send_photo

router = Router(name="Rates")


@router.message(F.text.in_(USER_RATE_BUTTONS))
async def rate_user_button_handler(message: Message, session: AsyncSession, state: FSMContext, user: User):
    """
    Обработка кнопок оценки и угадывания возрасты анкеты
    """
    await react_for_user_rate(message, user, state, session)
    await send_photo(message, user, session, state)
