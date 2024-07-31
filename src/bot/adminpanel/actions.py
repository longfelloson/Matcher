from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users import crud as users_crud
from bot.users.schemas import UserStatus


async def ban_user(message: Message, user_id: int, session: AsyncSession) -> None:
    await users_crud.update_user(user_id, session, status=UserStatus.BLOCKED)
    await message.edit_text(f"Пользователь <b>{user_id}</b> был заблокирован ✅")


async def unban_user(message: Message, user_id: int, session: AsyncSession) -> None:
    await users_crud.update_user(user_id, session, status=UserStatus.BLOCKED)
    await message.edit_text(f"Пользователь <b>{user_id}</b> был разблокирован 🔓")
