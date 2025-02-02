import asyncio
import aio_pika

from bot.notifications.constants import NEW_USERS_QUEUE_NAME
from bot.notifications.new_users.utils import on_new_user
from config import settings 


async def read_new_users():
    connection = await aio_pika.connect_robust(settings.acqp_url)
    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(NEW_USERS_QUEUE_NAME, durable=True)
        await queue.consume(on_new_user)

        await asyncio.Future()
