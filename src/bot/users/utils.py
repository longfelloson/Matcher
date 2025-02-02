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
from bot.notifications.pending_users.counters import set_pending_user_counter
from bot.notifications.pending_users.options import (
    get_pending_user_options, set_pending_user_options
)
from bot.storage import USER_FOR_VIEW_KEY
from bot.users.enums.answers import SearchAnswer
from bot.users.rates import crud as rates_crud
from bot.texts.users import get_user_profile_caption
from bot.users import crud as users_crud
from bot.users.guesses.states import GuessesState
from bot.users.guesses import utils
from bot.users.guesses import crud as guesses_crud
from bot.users.locations import get_nearest_user
from bot.users.models import User
from bot.users.rates.states import RateState
from bot.users.rates.utils import send_user_to_rate
from bot.users.search.options import get_search_options


async def get_user_from_redis(state: FSMContext, session: AsyncSession) -> User:
    data = await state.get_data()
    user_for_view = await users_crud.get_user_by_id(
        data.get("user_for_view_id"), session
    )
    return user_for_view


async def get_users_for_view(
    rated_users_ids: Sequence[int],
    guessed_users_ids: Sequence[int],
    user: User,
    session: AsyncSession,
) -> List[User]:
    search_options = get_search_options(
        rated_users_ids,
        guessed_users_ids,
        searcher=user,
    )

    for options in search_options:
        found_users = await users_crud.get_user_by_options(session, options)
        if found_users:
            return found_users

    return []


async def send_user_to_react(
    message: Message,
    viewer: User,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    guessed_users_ids = (
        await guesses_crud.get_guessed_users_ids(viewer.id, session)
    )
    rated_users_ids = (
        await rates_crud.get_rated_users_ids(viewer.id, session)
    )
    users_for_view = await get_users_for_view(
        rated_users_ids, guessed_users_ids, viewer, session
    )
    if not users_for_view:
        options = get_pending_user_options(viewer)

        await set_pending_user_counter(viewer.id)
        await set_pending_user_options(viewer, options)

        no_users_answer = await message.answer(
            SearchAnswer.no_users_for_view, reply_markup=main_keyboard()
        )
        return no_users_answer

    viewed = users_for_view[0]
    caption = get_user_profile_caption(viewer, viewed)

    if viewer.location:
        viewed = get_nearest_user(viewer, users_for_view)

    was_viewed_guessed = (
        utils.was_user_guessed(
            user_to_guess=viewed, 
            guessed_users_ids=guessed_users_ids
        )
    )
    if viewer.config.guess_age and not was_viewed_guessed:
        await state.set_state(GuessesState.user_age)
        await utils.send_user_to_guess(viewer, viewed, caption)
    else:
        await state.set_state(RateState.user)
        await send_user_to_rate(viewer, viewed, caption)

    await state.set_data({USER_FOR_VIEW_KEY: viewed.id})


async def send_user_to_view(
    photo: str,
    caption: str,
    keyboard=None,
    chat_id: Union[str, int] = None,
    message: Message = None,
) -> Message:
    if chat_id:
        return await bot.send_photo(
            chat_id, photo, caption=caption, reply_markup=keyboard
        )
    return await message.answer_photo(photo, caption, reply_markup=keyboard)
