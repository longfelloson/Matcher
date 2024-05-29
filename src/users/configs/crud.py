from sqlalchemy import update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.configs.models import UserConfig
from src.users.configs.schemas import UserConfig as UserConfigSchema


async def update_user_config(user_id: int, column: str, session: AsyncSession) -> UserConfig:
    """
    Обновление колонки пользовательского конфига
    """
    config = await get_user_config(user_id, session)
    new_value = False if getattr(config, column) else True

    await session.execute(update(UserConfig).where(UserConfig.user_id == user_id).values(**{column: new_value}))
    await session.commit()


async def get_user_config(user_id: int, session: AsyncSession) -> UserConfig:
    """
    Получение пользовательского конфига
    """
    config = await session.execute(select(UserConfig).where(UserConfig.user_id == user_id))
    return config.scalar_one()


async def add_user_config(user_config: UserConfigSchema, session: AsyncSession) -> UserConfig:
    """
    Добавление пользовательского конфига
    """
    await session.execute(insert(UserConfig).values(**user_config.model_dump()))
    await session.commit()
