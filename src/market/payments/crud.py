from pydantic import UUID4
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from market.payments.models import Payment
from market.payments.schemas import CreatePayment


async def create_payment(
    data: CreatePayment, 
    user_id: int, 
    session: AsyncSession,
) -> None:
    await session.execute(
        insert(Payment).values(**data.model_dump(), user_id=user_id)
    )
    await session.commit()


async def get_payment(payment_id: UUID4, session: AsyncSession) -> Payment:
    payment = await session.execute(
        select(Payment).where(Payment.id == payment_id)
    )
    return payment.scalar_one()


async def get_payments(
    offset: int, 
    limit: int, 
    session: AsyncSession
) -> list[Payment]:
    payments = await session.execute(
        select(Payment).offset(offset).limit(limit)
    )
    return payments.scalars().all()


async def update_payment(payment_id: int, session: AsyncSession, **values):
    await session.execute(
        update(Payment).where(Payment.id == payment_id).values(**values)
    )
    await session.commit()
