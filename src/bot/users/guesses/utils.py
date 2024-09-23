from typing import List, Set

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot
from bot.users import crud as users_crud
from bot.users.guesses import crud
from bot.users.guesses.enums import Answer
from bot.users.guesses.keyboards import rate_user_keyboard, guess_user_age_keyboard
from bot.users.guesses.schemas import Guess
from bot.users.models import User
from bot.users.rates.states import RateState
from bot.users.registration.enums.age import AgeGroup

DEFAULT_AGE_GUESS_SCORE = 0.0
CLOSE_AGE_GUESS_SCORE = 2.5
SAME_AGE_GUESS_SCORE = 5
DEFAULT_DELAY = 0.3


def get_guess_points(user_age_guess: int, user_for_view: User) -> float | int:
    """Возвращает баллы, которые получит человек за его попытку угадать возраст"""
    return SAME_AGE_GUESS_SCORE if user_age_guess == user_for_view.age else DEFAULT_AGE_GUESS_SCORE


async def react_for_user_guess(
        message: Message,
        user: User,
        session: AsyncSession,
        user_for_view: User,
        state: FSMContext,
) -> None:
    """Добавление пользовательского угадывания в базу и нужная реакция на него"""
    points = get_guess_points(
        user_age_guess=int(message.text), user_for_view=user_for_view
    )
    guess = Guess(
        guesser=user.user_id, guessed=user_for_view.user_id, points=points
    )
    answer = "Теперь оцени анкету ⤴️\n\n"

    await crud.add_guess(guess, session)
    await users_crud.increase_user_points(user.user_id, points, session)

    if points > 0:
        answer = f"(+{points} 🎈) {answer}"

    await state.set_state(RateState.user)
    await message.answer(answer, reply_markup=rate_user_keyboard())


async def get_guessed_users_ids(user_id: int, session: AsyncSession) -> Set[int]:
    guesses = await crud.get_user_guesses(user_id, session)
    return set(guess.guessed for guess in guesses)


async def send_user_to_guess(
        guesser: User,
        guessed: User,
        caption: str,
) -> None:
    """Отправляет пользователя для угадывания его возраста"""
    photo = await bot.send_photo(
        chat_id=guesser.user_id,
        caption=caption,
        photo=guessed.photo_url
    )
    guessed_age_group_name = AgeGroup.get_group_by_age(guessed.age).name
    await photo.answer(
        text=Answer.guess_age,
        reply_markup=guess_user_age_keyboard(guessed_age_group_name)
    )


def was_user_guessed(user_to_guess: User, guessed_users_ids: List[int]) -> bool:
    return user_to_guess.user_id in guessed_users_ids
