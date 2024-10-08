from typing import (
    List,
    Sequence,
    Union,
)

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.loader import bot
from bot.texts.users import get_user_profile_caption
from bot.users import crud as users_crud
from bot.users.guesses.enums import Answer
from bot.users.guesses.states import GuessesState
from bot.users.guesses.utils import (
    get_guessed_users_ids,
    was_user_guessed,
    send_user_to_guess,
)
from bot.users.locations import get_nearest_user
from bot.users.models import User
from bot.users.rates.states import RateState
from bot.users.rates.utils import get_rated_users_ids, send_user_to_rate
from bot.users.search import get_search_options


async def get_user_for_view(state: FSMContext, session: AsyncSession) -> User:
    """Получение пользователя для просмотра из Redis"""
    data = await state.get_data()
    user_for_view = await users_crud.get_user(data.get("user_for_view_id"), session)
    return user_for_view


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
        return await message.answer(Answer.not_user_for_guess, reply_markup=main_keyboard())

    user_for_view = users_for_view[0]
    caption = get_user_profile_caption(user, user_for_view)

    if user.location:
        user_for_view = get_nearest_user(user, users_for_view)

    if user.config.guess_age and not was_user_guessed(user_for_view, guessed_users_ids):
        await state.set_state(GuessesState.user_age)
        await send_user_to_guess(user, user_for_view, caption)
    else:
        await state.set_state(RateState.user)
        await send_user_to_rate(user, user_for_view, caption)

    await state.set_data({"user_for_view_id": user_for_view.user_id})


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
