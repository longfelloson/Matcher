from typing import Optional, List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users.guesses.models import Guess
from bot.users.guesses.schemas import Guess as GuessSchema


async def add_guess(guess: GuessSchema, session: AsyncSession) -> None:
    await session.execute(insert(Guess).values(**guess.model_dump()))
    await session.commit()


async def get_user_guesses(
    user_id: int, session: AsyncSession
) -> List[Optional[Guess]]:
    rates = await session.execute(select(Guess).where(Guess.guesser_user_id == user_id))
    return rates.scalars().all()


async def get_guessed_users_ids(
    user_id: int, session: AsyncSession
) -> List[Optional[int]]:
    users_ids = await session.execute(
        select(Guess.guessed_user_id).where(Guess.guesser_user_id == user_id)
    )
    return users_ids.scalars().all()
