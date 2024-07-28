from typing import Optional, List

from sqlalchemy import insert, select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages.guesses.models import Guess
from bot.messages.guesses.schemas import Guess as GuessSchema
from bot.messages.rates.models import Rate
from bot.users.models import User
from config import settings


async def add_guess(guess: GuessSchema, session: AsyncSession) -> None:
    """
    Добавление пользовательского угадывания в базу
    """
    await session.execute(insert(Guess).values(**guess.model_dump()))
    await session.commit()


async def get_guess(guess_id: int, session: AsyncSession) -> Guess:
    """
    Получение оценки из базы
    """
    guess = await session.execute(select(Guess).where(Guess.id_ == guess_id))
    return guess.scalar_one()


async def get_user_guesses(user_id: int, session: AsyncSession) -> Optional[List[Guess]]:
    """
    Получение пользовательских оценок
    """
    rates = await session.execute(select(Guess).where(Guess.guesser == user_id))
    return rates.scalars().all()


async def get_user_for_rate(user: User, user_rates: List[Rate], session: AsyncSession):
    """
    Получение анкеты пользователя для оценки
    """
    conditions = [
        User.user_id != user.user_id,
        User.user_id.not_in(set(rate.rated for rate in user_rates)),
        User.gender == user.preferred_gender,
        User.age.in_(settings.BOT.GROUPS_AGES[user.preferred_age_group]),
    ]
    user_for_rate = await session.execute(select(User).where(and_(*conditions)).limit(1).order_by(func.random()))
    return user_for_rate.scalar_one_or_none()
