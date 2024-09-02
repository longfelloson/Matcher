from typing import Optional, List

from sqlalchemy import insert, select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages.guesses.models import Guess
from bot.messages.guesses.schemas import Guess as GuessSchema


async def add_guess(guess: GuessSchema, session: AsyncSession) -> None:
    await session.execute(insert(Guess).values(**guess.model_dump()))
    await session.commit()


async def get_guess(guess_id: int, session: AsyncSession) -> Guess:
    guess = await session.execute(select(Guess).where(Guess.id_ == guess_id))
    return guess.scalar_one()


async def get_user_guesses(
        user_id: int, session: AsyncSession
) -> List[Optional[Guess]]:
    rates = await session.execute(select(Guess).where(Guess.guesser == user_id))
    return rates.scalars().all()
