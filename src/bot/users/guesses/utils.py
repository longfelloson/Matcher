from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot
from bot.users.guesses import crud
from bot.users.guesses.answers import Answer
from bot.users.guesses.constants import DEFAULT_AGE_GUESS_SCORE, SAME_AGE_GUESS_SCORE
from bot.users.guesses.keyboards import guess_age_buttons_keyboard
from bot.users.models import User
from bot.users.search.utils import get_age_range
from config import settings


def get_points_for_user_guess(
    user_age_guess: int, user_for_view: User
) -> int | float:
    return (
        SAME_AGE_GUESS_SCORE if user_age_guess == user_for_view.age
        else DEFAULT_AGE_GUESS_SCORE
    )


def convert_points_to_currency(score: int | float) -> float:
    return score / settings.MARKET_EXCHANGE_RATE


async def get_guessed_users_ids(user_id: int, session: AsyncSession) -> set[int]:
    guesses = await crud.get_user_guesses(user_id, session)
    return set(guess.guessed_user_id for guess in guesses)


async def send_user_to_guess(
    guesser: User,
    guessed: User,
    caption: str,
) -> None:
    photo = await bot.send_photo(
        chat_id=guesser.id, caption=caption, photo=guessed.photo_url
    )
    age_range = get_age_range(guesser.age)
    if guessed.age not in age_range:
        age_range = get_age_range(guessed.age, shift=True)
    
    await photo.answer(
        text=Answer.guess_age, 
        reply_markup=guess_age_buttons_keyboard(age_range)
    )


def was_user_guessed(user_to_guess: User, guessed_users_ids: list[int]) -> bool:
    return user_to_guess.id in guessed_users_ids
