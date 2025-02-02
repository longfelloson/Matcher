from bot.notifications.pending_users.constants import START_COUNTER_VALUE
from bot.storage import storage
from bot.notifications.keys import USER_COUNTER_KEY


async def set_pending_user_counter(user_id: int | str) -> None:
    key = USER_COUNTER_KEY.format(user_id)
    counter = await storage.redis.get(key)
    if not counter:
        await storage.redis.set(key, value=START_COUNTER_VALUE)


async def get_pending_user_counter(user_id: int | str) -> int:
    key = USER_COUNTER_KEY.format(user_id)
    response = await storage.redis.get(key)

    counter_value = int(response.decode('utf-8'))
    return counter_value


async def update_pending_user_counter(user_id: int | str):
    counter = await get_pending_user_counter(user_id)
    counter += 1
    
    key = USER_COUNTER_KEY.format(user_id)
    await storage.redis.set(key, value=counter)


async def remove_pending_user_counter(user_id: int | str) -> None:
    key = USER_COUNTER_KEY.format(user_id)
    await storage.redis.delete(key)
    