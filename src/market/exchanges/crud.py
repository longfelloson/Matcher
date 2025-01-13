from typing import Optional
from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from market.exchanges.models import Exchange
from market.exchanges.schemas import CreateExchange


async def create_exchange(
    data: CreateExchange,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await session.execute(insert(Exchange).values(
        **data.model_dump(), user_id=user_id)
    )
    await session.commit()


async def get_exchanges(
    offset: int, 
    limit: int, 
    session: AsyncSession
) -> list[Optional[Exchange]]:
    exchanges = await session.execute(
        select(Exchange).offset(offset).limit(limit)
    )
    return exchanges.scalars().all()


async def get_exchange(
    exchange_id: UUID4, session: AsyncSession
) -> Optional[Exchange]:
    exchange = await session.execute(
        select(Exchange).where(Exchange.id == exchange_id)
    )
    return exchange.scalar_one_or_none()


async def delete_exchange(exchange_id: UUID4, session: AsyncSession) -> None:
    await session.execute(delete(Exchange).where(Exchange.id == exchange_id))
    await session.commit()
    