from typing import List, Tuple

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.messages.guesses.keyboards import guess_user_age_keyboard, rate_user_keyboard
from bot.messages.guesses.schemas import Answers
from bot.messages.guesses.states import GuessesStates
from bot.messages.rates import crud as rates_crud
from bot.messages.rates.models import Rate
from bot.messages.rates.states import RatesStates
from bot.text.utils import get_user_profile_caption
from bot.users import crud as users_crud
from bot.users.geo.utils import get_nearest_user
from bot.users.models import User
from bot.users.schemas import UserStatus
from config import settings

DEFAULT_AGE_GUESS_SCORE = 0.0
CLOSE_AGE_GUESS_SCORE = 2.5
SAME_AGE_GUESS_SCORE = 5
LOCATION_SPLIT_SYMBOL = "*"


def get_search_options(user_rates: List[Rate], searcher: User) -> Tuple[List, List]:
    """
    Получение условий поиска пользователей для просмотра
    """
    common_options = [
        User.user_id != searcher.user_id,
        User.status == UserStatus.ACTIVE,
        User.user_id.not_in(set(rate.rated for rate in user_rates)),
        User.gender == searcher.preferred_gender,
        User.age.in_(settings.BOT.GROUPS_AGES[searcher.preferred_age_group]),
    ]
    specific_options = common_options + [
        User.city == searcher.city,
    ]
    return specific_options, common_options


async def get_users_for_view(user: User, session: AsyncSession) -> List[User]:
    """
    Получение пользователей, из которых можно выбрать пользователя для просмотра
    """
    user_rates = await rates_crud.get_user_rates(user.user_id, session)
    specific_search_options, common_search_options = get_search_options(
        user_rates, user
    )

    users = await users_crud.get_users(session, options=specific_search_options)
    if not users:
        users = await users_crud.get_users(session, options=common_search_options)

    return users


async def send_user_for_view(
    message: Message, user: User, session: AsyncSession, state: FSMContext
) -> None:
    """
    Отправка фотографии пользователя на оценку
    """
    users_for_view = await get_users_for_view(user, session)
    if not users_for_view:
        await message.answer(Answers.NOT_USER_FOR_GUESS, reply_markup=main_keyboard())
        return

    user_for_view = users_for_view[0]

    if user.location:
        user_for_view = get_nearest_user(user, users_for_view)

    if user.config.guess_age:
        answer = Answers.GUESS_AGE
        keyboard = guess_user_age_keyboard(user)
        await state.set_state(GuessesStates.guess_user_age)
    else:
        answer = Answers.RATE_USER
        keyboard = rate_user_keyboard()
        await state.set_state(RatesStates.rate_user)

    caption = get_user_profile_caption(user, user_for_view)

    await state.set_data({"user_for_rate": user_for_view})
    photo = await message.answer_photo(user_for_view.photo_url, caption)
    await photo.reply(answer, reply_markup=keyboard)
