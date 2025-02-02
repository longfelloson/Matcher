import asyncio
import aio_pika

from bot.notifications.constants import NOTIFICATIONS_QUEUE_NAME
from bot.notifications.utils import on_notification
from config import settings 


async def read_notifications():
    connection = await aio_pika.connect_robust(settings.acqp_url)
    async with connection:
        channel = await connection.channel()
        
        queue = await channel.declare_queue(
            NOTIFICATIONS_QUEUE_NAME, durable=True
        )
        await queue.consume(on_notification)

        await asyncio.Future()
