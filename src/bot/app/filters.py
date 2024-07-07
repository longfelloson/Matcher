from aiogram.filters import Filter

from config import settings


class UserAdminFilter(Filter):
    async def __call__(self, data: dict):
        """
        Is user admin
        """
        return data['user'].user_id in settings.bot.ADMINS_IDS
