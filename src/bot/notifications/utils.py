import json
from aio_pika import IncomingMessage

from bot.loader import bot
from bot.notifications.schemas import Notification


async def send_notification(notification: Notification) -> None:
    await bot.send_message(notification.user_id, notification.text)


async def on_notification(message: IncomingMessage) -> None:
    async with message.process():
        json_data = json.loads(message.body.decode())

    notification = Notification(**json_data)
    await send_notification(notification)
