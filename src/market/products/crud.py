from typing import List

from sqlalchemy import insert, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from market.products.models import UserProduct, Product


async def create_user_product(
        user_id: int, product_id: int, session: AsyncSession
) -> None:
    """
    Добавляет товар пользователя полученный в результате обмена
    """
    await session.execute(
        insert(UserProduct).values(user_id=user_id, product_id=product_id)
    )
    await session.commit()


async def get_products(
        offset: int, limit: int, user_id: int | None, session: AsyncSession
) -> List:
    """
    Получение всех товаров. Если указан ID пользователя - получение товаров пользователя
    """
    stmt = select(Product)
    if user_id:
        stmt = select(UserProduct).where(UserProduct.user_id == user_id)

    result = await session.execute(stmt.offset(offset).limit(limit))
    return result.scalars().all()


async def get_product(
        product_id: int, session: AsyncSession, user_id: int = None
) -> Product | UserProduct:
    """
    Получение товара. Если указан ID пользователя - получение пользовательского товара
    """
    stmt = select(UserProduct if user_id else Product)
    if user_id:
        stmt = stmt.where(
            and_(UserProduct.user_id == user_id), UserProduct.product_id == product_id
        )
    else:
        stmt = stmt.where(Product.id_ == product_id)

    result = await session.execute(stmt)
    return result.scalar_one()
