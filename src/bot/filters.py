from aiogram.filters import Filter

from src import config


class UserAdminFilter(Filter):
    async def __call__(self, data: dict):
        """
        Проверка, является ли пользователь админом
        """
        return data['user'].user_id in config.ADMINS_IDS
