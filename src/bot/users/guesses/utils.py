from typing import (
    List,
    Set,
    Union,
)

from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot
from bot.users.guesses import crud
from bot.users.guesses.answers import Answer
from bot.users.guesses.keyboards import guess_age_buttons_keyboard
from bot.users.models import User
from bot.users.search import get_age_range

DEFAULT_AGE_GUESS_SCORE = 0.0
CLOSE_AGE_GUESS_SCORE = 2.5
SAME_AGE_GUESS_SCORE = 5
DEFAULT_DELAY = 0.3


def get_points_for_user_guess(
    user_age_guess: int, user_for_view: User
) -> Union[int, float]:
    return (
        SAME_AGE_GUESS_SCORE
        if user_age_guess == user_for_view.age
        else DEFAULT_AGE_GUESS_SCORE
    )


async def get_guessed_users_ids(user_id: int, session: AsyncSession) -> Set[int]:
    guesses = await crud.get_user_guesses(user_id, session)
    return set(guess.guessed for guess in guesses)


async def send_user_to_guess(
    guesser: User,
    guessed: User,
    caption: str,
) -> None:
    photo = await bot.send_photo(
        chat_id=guesser.id, caption=caption, photo=guessed.photo_url
    )
    age_range = get_age_range(guessed.age)
    await photo.answer(
        text=Answer.guess_age, reply_markup=guess_age_buttons_keyboard(age_range)
    )


def was_user_guessed(user_to_guess: User, guessed_users_ids: List[int]) -> bool:
    return user_to_guess.id in guessed_users_ids
