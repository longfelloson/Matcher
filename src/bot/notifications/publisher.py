import aio_pika

from bot.notifications.constants import NOTIFICATIONS_QUEUE_NAME
from bot.notifications.schemas import Notification

from config import settings


async def publish_notification(notification: Notification) -> None:
    connection = await aio_pika.connect_robust(settings.acqp_url)

    async with connection:
        channel = await connection.channel()

        body = notification.model_dump_json().encode()
        message = aio_pika.Message(body=body)

        await channel.default_exchange.publish(
            message, NOTIFICATIONS_QUEUE_NAME
        )
        