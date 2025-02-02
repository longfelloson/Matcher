from typing import Optional, List, Union

from sqlalchemy import insert, update, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from bot.users.enums.statuses import UserStatus
from bot.users.models import User
from bot.users.registration.schemas import UserRegistrationInfo

DEFAULT_USERS_LIMIT = 100


async def create_user(user: UserRegistrationInfo, session: AsyncSession) -> None:
    await session.execute(insert(User).values(**user.model_dump()))
    await session.commit()


async def update_user(user_id: int, session: AsyncSession, **user_info) -> None:
    await session.execute(update(User).where(User.id == user_id).values(**user_info))
    await session.commit()


async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[User]:
    user = await session.execute(select(User).where(User.id == user_id))
    return user.scalar_one_or_none()


async def increase_user_points(
    user_id: int,
    points: Union[int, float],
    session: AsyncSession,
) -> None:
    """Увеличение очков пользователя"""
    await session.execute(
        update(User).where(User.id == user_id).values(points=User.points + points)
    )
    await session.commit()


async def decrease_user_points(
    user_id: int, points: Union[int, float], session: AsyncSession
) -> None:
    """Уменьшение очков пользователя"""
    await session.execute(
        update(User).where(User.id == user_id).values(points=User.points - points)
    )
    await session.commit()


async def get_user_by_options(
    session: AsyncSession,
    options: list,
    limit: int = DEFAULT_USERS_LIMIT,
) -> List[User]:
    """Получение пользователей по заданным условиям"""
    stmt = select(User).limit(limit)
    if options:
        stmt = stmt.where(and_(*options))

    users = await session.execute(stmt)
    return users.scalars().all()


async def get_user_points(user_id: int, session: AsyncSession) -> Union[int, float]:
    """Возвращает количество очков пользователя"""
    points = await session.execute(select(User.points).where(User.id == user_id))
    return points.scalar_one()


async def get_users_amount(
    session: AsyncSession, users_status: UserStatus = None
) -> int:
    stmt = select(count(User.id))
    if users_status:
        stmt = stmt.where(User.status == users_status)

    users_amount = await session.execute(stmt)
    return users_amount.scalar_one()
