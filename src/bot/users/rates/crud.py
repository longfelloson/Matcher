from typing import List, Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users.rates.models import Rate
from bot.users.rates.schemas import Rate as RateSchema


async def add_rate(rate: RateSchema, session: AsyncSession) -> None:
    await session.execute(insert(Rate).values(**rate.model_dump()))
    await session.commit()


async def get_user_rates(user_id: int, session: AsyncSession) -> List[Rate]:
    rates = await session.execute(select(Rate).where(Rate.rater_user_id == user_id))
    return rates.scalars().all()


async def get_rater_users_ids(
    user_id: int, session: AsyncSession
) -> List[Optional[int]]:
    users_ids = await session.execute(
        select(Rate.rater_user_id).where(Rate.rated_user_id == user_id)
    )
    return users_ids.scalars().all()


async def get_rated_users_ids(
    user_id: int, session: AsyncSession
) -> List[Optional[int]]:
    users_ids = await session.execute(
        select(Rate.rated_user_id).where(Rate.rater_user_id == user_id)
    )
    return users_ids.scalars().all()
