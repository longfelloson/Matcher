from typing import List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages.rates.models import Rate
from bot.messages.rates.schemas import Rate as RateSchema


async def add_rate(rate: RateSchema, session: AsyncSession) -> None:
    await session.execute(insert(Rate).values(**rate.model_dump()))
    await session.commit()


async def get_user_rates(user_id: int, session: AsyncSession) -> List[Rate]:
    rates = await session.execute(select(Rate).where(Rate.rater == user_id))
    return rates.scalars().all()
