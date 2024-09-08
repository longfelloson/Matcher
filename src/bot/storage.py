from aiogram.fsm.storage.redis import RedisStorage

from config import settings

storage = RedisStorage.from_url(settings.redis_url)
