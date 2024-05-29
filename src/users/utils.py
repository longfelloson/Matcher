import asyncio
from typing import List

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src import config
from src.bot.keyboards import main_keyboard

from src.guesses import crud
from src.guesses.keyboards import guess_user_age_keyboard, rate_user_keyboard
from src.guesses.schemas import Answers
from src.guesses.states import GuessesStates
from src.rates import crud as rates_crud
from src.rates.models import Rate
from src.rates.states import RatesStates
from src.text.utils import get_user_profile_caption
from src.users import crud as users_crud
from src.users.geo.utils import get_nearest_user
from src.users.models import User
from src.users.schemas import UserStatuses

DEFAULT_AGE_GUESS_SCORE = 0.0
CLOSE_AGE_GUESS_SCORE = 2.5
SAME_AGE_GUESS_SCORE = 5
DEFAULT_DELAY = 0.3
LOCATION_SPLIT_SYMBOL = "*"


def get_search_conditions(user_rates: List[Rate], searcher: User) -> List:
    """
    Получение условий поиска пользователей для просмотра
    """
    conditions = [
        User.user_id != searcher.user_id,
        User.status == UserStatuses.ACTIVE,
        User.user_id.not_in(set(rate.rated for rate in user_rates)),
        User.gender == searcher.preferred_gender,
        User.city == searcher.city,
        User.age.in_(config.GROUPS_AGES[searcher.preferred_age_group]),
    ]
    return conditions


async def send_photo(message: Message, user: User, session: AsyncSession, state: FSMContext) -> None:
    """
    Отправка фотографии пользователя на оценку
    """
    user_rates = await rates_crud.get_user_rates(user.user_id, session)
    users = await users_crud.get_users(session, conditions=get_search_conditions(user_rates, user))
    if not users:
        await message.answer(Answers.NOT_USER_FOR_GUESS, reply_markup=main_keyboard())
        return

    user_for_view = users[0]

    if user.location:
        user_for_view = get_nearest_user(user, users)

    if user.config.guess_age:
        answer = Answers.GUESS_AGE
        keyboard = guess_user_age_keyboard(user)
        await state.set_state(GuessesStates.guess_user_age)
    else:
        answer = Answers.RATE_USER
        keyboard = rate_user_keyboard()
        await state.set_state(RatesStates.rate_user)

    caption = get_user_profile_caption(user_for_view)

    await asyncio.sleep(DEFAULT_DELAY)
    await state.set_data({"user_for_rate": user_for_view})

    photo = await message.answer_photo(user_for_view.photo_file_id, caption)
    await photo.reply(answer, reply_markup=keyboard)
