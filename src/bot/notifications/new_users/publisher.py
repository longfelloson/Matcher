import aio_pika

from bot.notifications.constants import NEW_USERS_QUEUE_NAME
from bot.notifications.new_users.schemas import NewUser
from bot.users.registration.schemas import UserRegistrationInfo
from config import settings


async def publish_new_user(registration_info: UserRegistrationInfo) -> None:
    connection = await aio_pika.connect_robust(settings.acqp_url)

    async with connection:
        channel = await connection.channel()

        new_user = NewUser(**registration_info.model_dump())

        body = new_user.model_dump_json()
        message = aio_pika.Message(body=body.encode())

        await channel.default_exchange.publish(message, NEW_USERS_QUEUE_NAME)
        