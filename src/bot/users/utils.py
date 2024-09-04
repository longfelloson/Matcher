from typing import List, Tuple, Sequence, Union

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.loader import bot
from bot.messages.guesses.enums import Answer
from bot.messages.guesses.keyboards import guess_user_age_keyboard, rate_user_keyboard
from bot.messages.guesses.states import GuessesStates
from bot.messages.rates import crud as rates_crud
from bot.messages.rates.states import RatesStates
from bot.texts.users import get_user_profile_caption
from bot.users import crud as users_crud
from bot.users.enums import UserStatus, AgeGroup
from bot.users.geo.utils import get_nearest_user
from bot.users.models import User
from bot.users.schemas import User as UserSchema

DEFAULT_AGE_GUESS_SCORE = 0.0
CLOSE_AGE_GUESS_SCORE = 2.5
SAME_AGE_GUESS_SCORE = 5


def get_user_schema_from_message(user_message: Message) -> UserSchema:
    """
    Получение схемы пользователя по его сообщению
    """
    return UserSchema(
        user_id=user_message.chat.id,
        username=user_message.chat.username,
    )


def get_search_options(rated_users_ids: Sequence[int], searcher: User) -> Tuple[List, List, List]:
    """
    Получение условий поиска пользователей для просмотра
    """
    minimal_options = [
        User.user_id != searcher.user_id,
        User.status == UserStatus.active,
        User.user_id.not_in(rated_users_ids),
        User.gender == searcher.preferred_gender,
    ]
    common_options = minimal_options + [
        User.age.in_(AgeGroup.get_group_by_age(searcher.age).value)
    ]
    specific_options = common_options + [
        User.city == searcher.city
    ]
    return specific_options, common_options, minimal_options


async def get_users_for_view(user: User, session: AsyncSession) -> List[User]:
    """
    Получение пользователей, из которых можно выбрать пользователя для просмотра
    """
    user_rates = await rates_crud.get_user_rates(user.user_id, session)
    rated_users_ids = set(rate.rated for rate in user_rates)

    specific_search_options, common_search_options, minimal_options = get_search_options(rated_users_ids, user)

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
    """
    Отправка фотографии пользователя на оценку
    """
    users_for_view = await get_users_for_view(user, session)
    if not users_for_view:
        await message.answer(Answer.not_user_for_guess, reply_markup=main_keyboard())
        return

    user_for_view = users_for_view[0]

    if user.location:
        user_for_view = get_nearest_user(user, users_for_view)

    if user.config.guess_age:
        answer = Answer.guess_age
        keyboard = guess_user_age_keyboard(age_group=AgeGroup.get_group_by_age(user_for_view.age))
        await state.set_state(GuessesStates.user_age)
    else:
        answer = Answer.rate_user
        keyboard = rate_user_keyboard()
        await state.set_state(RatesStates.rate_user)

    caption = get_user_profile_caption(user, user_for_view)

    await state.set_data({"user_for_rate": user_for_view})
    photo = await send_user_to_view(user_for_view.photo_url, caption, message=message)
    await photo.answer(answer, reply_markup=keyboard)


async def send_user_to_view(
        photo: str,
        caption: str,
        keyboard=None,
        chat_id: Union[str, int] = None,
        message: Message = None,
) -> Message:
    if not chat_id and not message:
        raise ValueError("Какой-то из аргументов должен быть заполнен для отправки фото!")

    if chat_id:
        return await bot.send_photo(chat_id, photo, caption=caption, reply_markup=keyboard)
    return await message.answer_photo(photo, caption, reply_markup=keyboard)
