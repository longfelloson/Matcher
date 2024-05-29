from typing import Optional

from sqlalchemy import insert, update, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.schemas import User as UserSchema

DEFAULT_USERS_LIMIT = 100


async def create_user(user: UserSchema, session: AsyncSession) -> None:
    """
    Добавление пользователя в базу
    """
    await session.execute(insert(User).values(**user.model_dump()))
    await session.commit()


async def update_user(user_id: int, session: AsyncSession, **user_info) -> None:
    """
    Обновление пользовательской информации
    """
    await session.execute(update(User).where(User.user_id == user_id).values(**user_info))
    await session.commit()


async def get_user(user_id: int, session: AsyncSession) -> Optional[User]:
    """
    Получение пользователя по его ID
    """
    user = await session.execute(select(User).where(User.user_id == user_id))
    return user.scalar_one_or_none()


async def increase_user_points(user_id: int, points: int | float, session: AsyncSession) -> None:
    """
    Увеличение очков пользователя
    """
    await session.execute(update(User).where(User.user_id == user_id).values(points=User.points + points))
    await session.commit()


async def decrease_user_points(user_id: int, points: int | float, session: AsyncSession) -> None:
    """
    Уменьшение очков пользователя
    """
    await session.execute(update(User).where(User.user_id == user_id).values(points=User.points - points))
    await session.commit()


async def get_users(session: AsyncSession, limit: int = DEFAULT_USERS_LIMIT, conditions: dict = None):
    """
    Получение пользователей
    """
    stmt = select(User).limit(limit)
    if conditions:
        stmt = stmt.where(and_(*conditions))

    users = await session.execute(stmt)
    return users.scalars().all()
