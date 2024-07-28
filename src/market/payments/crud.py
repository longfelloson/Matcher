from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from market.payments.models import Payment
from market.payments.schemas import CreatePayment


async def get_payment(payment_id: int, session: AsyncSession) -> Payment:
    """
    Gets payment by payment id
    """
    payment = await session.execute(select(Payment).where(Payment.id_ == payment_id))
    return payment.scalar_one()


async def create_payment(data: CreatePayment, session: AsyncSession) -> int:
    """
    Creates payment and returns its id
    """
    id_ = await session.execute(insert(Payment).values(**data.model_dump()).returning(Payment.id_))
    await session.commit()

    return id_.scalar_one()


async def update_payment(payment_id: int, session: AsyncSession, **values):
    """
    Updates payment by payment id
    """
    await session.execute(update(Payment).where(Payment.id_ == payment_id).values(**values))
    await session.commit()
