from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from market.transactions.models import Transaction


async def create_transaction(type_: str, product_id: int, amount: int, session: AsyncSession) -> None:
    """
    Создает новую транзакцию (обмен баллов, покупка товаров и т.д.)
    """
    await session.execute(insert(Transaction).values(type_=type_, product_id=product_id, amount=amount))
    await session.commit()
