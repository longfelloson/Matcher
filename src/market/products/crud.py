from typing import List

from sqlalchemy import insert, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from market.products.models import UserProduct, Product


async def create_user_product(user_id: int, product_id: int, session: AsyncSession) -> None:
    """
    Adds a new user's product to the database
    """
    await session.execute(insert(UserProduct).values(user_id=user_id, product_id=product_id))
    await session.commit()


async def get_products(offset: int, limit: int, user_id: int | None, session: AsyncSession) -> List:
    """
    Gets all products from database. If user_id is provided, only user products
    """
    stmt = select(Product)
    if user_id:
        stmt = select(UserProduct).where(UserProduct.user_id == user_id)

    result = await session.execute(stmt.offset(offset).limit(limit))
    return result.scalars().all()


async def get_product(product_id: int, session: AsyncSession, user_id: int = None) -> Product | UserProduct:
    """
    Gets a single product from the database. If user_id is provided, only user product
    """
    stmt = select(UserProduct if user_id else Product)
    if user_id:
        stmt = stmt.where(and_(UserProduct.user_id == user_id), UserProduct.product_id == product_id)
    else:
        stmt = stmt.where(Product.id_ == product_id)

    result = await session.execute(stmt)
    return result.scalar_one()
