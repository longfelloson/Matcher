from typing import List, Optional
from pydantic import UUID4
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from market.purchases.models import Purchase
from market.purchases.schemas import CreatePurchase


async def create_purchase(
    data: CreatePurchase, user_id: int, session: AsyncSession
) -> None:
    await session.execute(insert(Purchase).values(**data.model_dump(), user_id=user_id))
    await session.commit()


async def get_purchases(
    offset: int, limit: int, session: AsyncSession
) -> List[Purchase]:
    purchases = await session.execute(select(Purchase).offset(offset).limit(limit))
    return purchases.scalars().all()


async def get_purchase(purchase_id: UUID4, session: AsyncSession) -> Optional[Purchase]:
    purchase = await session.execute(select(Purchase).where(Purchase.id == purchase_id))
    return purchase.scalar_one_or_none()
