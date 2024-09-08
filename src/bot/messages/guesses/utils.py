import asyncio
from typing import Any, List, Set

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot
from bot.messages.guesses import crud
from bot.messages.guesses.enums import Answer
from bot.messages.guesses.keyboards import rate_user_keyboard, guess_user_age_keyboard
from bot.messages.guesses.schemas import Guess
from bot.messages.registration.enums.age import AgeGroup
from bot.users import crud as users_crud
from bot.users.models import User

DEFAULT_AGE_GUESS_SCORE = 0.0
CLOSE_AGE_GUESS_SCORE = 2.5
SAME_AGE_GUESS_SCORE = 5
DEFAULT_DELAY = 0.3


async def update_state_data(state: FSMContext, key: str, value: Any) -> None:
    data = await state.get_data()
    data[key] = value
    await state.update_data(data)


def get_guess_points(user_age_guess: int, user_for_rate: User) -> float | int:
    """Возвращает баллы, которые получит человек за его попытку угадать возраст"""
    score = DEFAULT_AGE_GUESS_SCORE
    if user_age_guess == user_for_rate.age:
        score = SAME_AGE_GUESS_SCORE
    elif user_age_guess in [user_for_rate.age - 1, user_for_rate.age + 1]:
        score = CLOSE_AGE_GUESS_SCORE

    return score


async def react_for_user_guess(
    message: Message,
    user: User,
    session: AsyncSession,
    state: FSMContext
) -> None:
    """Добавление пользовательского угадывания в базу и нужная реакция на него"""
    data = await state.get_data()
    points = get_guess_points(int(message.text), data["user_for_rate"])

    guess = Guess(
        guesser=user.user_id, guessed=data["user_for_rate"].user_id, points=points
    )
    answer = Answer.get_age_guess_answer(user, data["user_for_rate"], points)

    await crud.add_guess(guess, session)
    await users_crud.increase_user_points(user.user_id, points, session)

    answer_message = await message.answer(answer)

    await asyncio.sleep(0.75)
    await answer_message.delete()
    await message.answer(f"Теперь оцени анкету ⤴️\n\n", reply_markup=rate_user_keyboard())


async def get_guessed_users_ids(user_id: int, session: AsyncSession) -> Set[int]:
    guesses = await crud.get_user_guesses(user_id, session)
    return set(guess.guessed for guess in guesses)


async def send_user_to_guess(guesser: User, guessed: User, caption: str) -> None:
    """Отправляет пользователя для угадывания его возраста"""
    photo = await bot.send_photo(
        chat_id=guesser.user_id,
        caption=caption,
        photo=guessed.photo_url
    )
    await photo.answer(
        text=Answer.guess_age,
        reply_markup=guess_user_age_keyboard(AgeGroup.get_group_by_age(guessed.age).name)
    )


def was_user_guessed(user_to_guess: User, guessed_users_ids: List[int]) -> bool:
    return user_to_guess.user_id in guessed_users_ids
