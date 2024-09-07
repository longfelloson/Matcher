from operator import and_
from typing import List, Tuple, Sequence, Union

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.loader import bot
from bot.messages.guesses.enums import Answer
from bot.messages.guesses.keyboards import guess_user_age_keyboard, rate_user_keyboard
from bot.messages.guesses.states import GuessesStates
from bot.messages.guesses import crud as guesses_crud
from bot.messages.guesses.utils import get_guessed_users_ids, was_user_guessed, send_user_to_guess
from bot.messages.rates import crud as rates_crud
from bot.messages.rates.states import RatesStates
from bot.messages.rates.utils import get_rated_users_ids, send_user_to_rate, was_user_rated
from bot.messages.registration.enums.age import AgeGroup
from bot.messages.registration.enums.gender import PreferredGender
from bot.texts.users import get_user_profile_caption
from bot.users import crud as users_crud
from bot.users.enums import UserStatus
from bot.users.geo.utils import get_nearest_user
from bot.users.models import User
from bot.users.schemas import User as UserSchema

DEFAULT_AGE_GUESS_SCORE = 0.0
CLOSE_AGE_GUESS_SCORE = 2.5
SAME_AGE_GUESS_SCORE = 5


def get_user_schema_from_message(user_message: Message) -> UserSchema:
    """Получение схемы пользователя по его сообщению"""
    return UserSchema(user_id=user_message.chat.id, username=user_message.chat.username)


def get_search_options(
    rated_users_ids: Sequence[int],
    guessed_users_ids: Sequence[int],
    searcher: User,
) -> Tuple[List, List, List]:
    """Получение условий поиска пользователей для просмотра"""
    minimal_options = [
        User.user_id != searcher.user_id,
        User.status == UserStatus.active,
    ]
    if searcher.config.guess_age:
        minimal_options += [
            and_(User.user_id.not_in(guessed_users_ids), User.user_id.not_in(rated_users_ids))
        ]
    else:
        minimal_options += [
            User.user_id.not_in(rated_users_ids)
        ]

    if searcher.preferred_gender != PreferredGender.both:
        minimal_options += [
            User.gender == searcher.preferred_gender
        ]

    common_options = minimal_options + [
        User.age.in_(AgeGroup.get_group_by_age(searcher.age).value)
    ]
    specific_options = common_options + [
        User.city == searcher.city
    ]
    return specific_options, common_options, minimal_options


async def get_users_for_view(
    rated_users_id: Sequence[int],
    guessed_users_ids: Sequence[int],
    user: User,
    session: AsyncSession,
) -> List[User]:
    """Получение пользователей, из которых можно выбрать пользователя для просмотра"""
    specific_search_options, common_search_options, minimal_options = get_search_options(
        rated_users_ids=rated_users_id,
        guessed_users_ids=guessed_users_ids,
        searcher=user,
    )
    users = await users_crud.get_users(session, options=specific_search_options)
    if not users:
        users = await users_crud.get_users(session, options=common_search_options)
    if not users:
        users = await users_crud.get_users(session, options=minimal_options)

    return users


async def send_user_to_react(
    message: Message,
    user: User,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    """Отправка фотографии пользователя на оценку"""
    guessed_users_ids = await get_guessed_users_ids(user.user_id, session)
    rated_users_ids = await get_rated_users_ids(user.user_id, session)

    users_for_view = await get_users_for_view(rated_users_ids, guessed_users_ids, user, session)
    if not users_for_view:
        await message.answer(Answer.not_user_for_guess, reply_markup=main_keyboard())
        return

    user_for_view = users_for_view[0]
    caption = get_user_profile_caption(user, user_for_view)

    if user.location:
        user_for_view = get_nearest_user(user, users_for_view)

    if user.config.guess_age and not was_user_guessed(user_for_view, guessed_users_ids):
        await state.set_state(GuessesStates.user_age)
        await send_user_to_guess(user, user_for_view, caption)
    else:
        await state.set_state(RatesStates.rate_user)
        await send_user_to_rate(user, user_for_view, caption)

    await state.set_data({"user_for_rate": user_for_view})


async def send_user_to_view(
    photo: str,
    caption: str,
    keyboard=None,
    chat_id: Union[str, int] = None,
    message: Message = None,
) -> Message:
    if not chat_id and not message:
        raise ValueError("Какой-то из аргументов должен быть заполнен для отправки пользователя!")

    if chat_id:
        return await bot.send_photo(chat_id, photo, caption=caption, reply_markup=keyboard)
    return await message.answer_photo(photo, caption, reply_markup=keyboard)
