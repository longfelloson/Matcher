from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.guesses import crud
from bot.guesses.keyboards import rate_user_keyboard
from bot.guesses.schemas import Answers, Guess
from bot.users import crud as users_crud
from bot.users.models import User

DEFAULT_AGE_GUESS_SCORE = 0.0
CLOSE_AGE_GUESS_SCORE = 2.5
SAME_AGE_GUESS_SCORE = 5
DEFAULT_DELAY = 0.3


async def update_state_data(state: FSMContext, key: str, value: Any) -> None:
    """
    Обновление даты состояние
    """
    data = await state.get_data()
    data[key] = value
    await state.update_data(data)


def get_rate_schema(score: int | float, user_id: int, rated_user_id: int) -> Guess:
    """
    Получение схемы оценки
    """
    return Guess(guesser=user_id, guessed=rated_user_id, score=score)


def get_guess_points(user_age_guess: int, user_for_rate: User) -> float | int:
    """
    Возвращает баллы, которые получит человек за его попытку угадать возраст
    """
    score = DEFAULT_AGE_GUESS_SCORE
    if user_age_guess == user_for_rate.age:
        score = SAME_AGE_GUESS_SCORE
    elif user_age_guess in [user_for_rate.age - 1, user_for_rate.age + 1]:
        score = CLOSE_AGE_GUESS_SCORE

    return score


async def react_for_user_guess(message: Message, user: User, session: AsyncSession, state: FSMContext) -> None:
    """
    Добавление пользовательского угадывания в базу
    """
    data = await state.get_data()
    points = get_guess_points(int(message.text), data['user_for_rate'])

    guess = Guess(
        guesser=user.user_id,
        guessed=data['user_for_rate'].user_id,
        points=points
    )
    answer = Answers.get_age_guess_answer(user, data['user_for_rate'], points)

    await crud.add_guess(guess, session)
    await users_crud.increase_user_points(user.user_id, points, session)
    await message.reply(answer, reply_markup=rate_user_keyboard())
