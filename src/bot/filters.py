from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users import crud as users_crud
from config import settings


class NotSolvedCaptchaFilter(Filter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        """

        """
        user_id = message.chat.id
        user = await users_crud.get_user(user_id, session)

        if not user:
            return True
        return False if user.is_captcha_solved else True


class UserAdminFilter(Filter):
    async def __call__(self, data: dict):
        """
        Is user admin
        """
        return data['user'].user_id in settings.bot.ADMINS_IDS
