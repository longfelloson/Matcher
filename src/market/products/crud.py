from typing import List
import uuid
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from market.products.models import Product
from market.products.schemas import CreateProduct


async def create_product(
    data: CreateProduct,
    img_url: str,
    session: AsyncSession,
) -> None:
    await session.execute(insert(Product).values(**data.model_dump(), img_url=img_url))
    await session.commit()


async def get_products(
    offset: int,
    limit: int,
    session: AsyncSession,
) -> List[Product]:
    products = await session.execute(select(Product).offset(offset).limit(limit))
    return products.scalars().all()


async def delete_product(product_id: uuid.uuid4, session: AsyncSession) -> None:
    await session.execute(delete(Product).where(Product.id == product_id))
    await session.commit()
