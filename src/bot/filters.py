from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users import crud as users_crud
from config import settings


class NotSolvedCaptchaFilter(Filter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        """
        Фильтр пользователей на предмет нерешенной капчи
        """
        user_id = message.chat.id
        user = await users_crud.get_user(user_id, session)

        if not user:
            return True
        return False if user.is_captcha_solved else True


class UserAdminFilter(Filter):
    async def __call__(self, message: Message):
        """
        Проверка, является ли пользователь админом
        """
        user_id = message.from_user.id
        return user_id in settings.admins_ids
