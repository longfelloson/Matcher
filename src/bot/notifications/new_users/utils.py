import json
from aio_pika import IncomingMessage

from bot.notifications.enums import NotificationText, NotificationType
from bot.notifications.new_users.schemas import NewUser
from bot.notifications.pending_users.constants import MAX_COUNTER_VALUE
from bot.notifications.pending_users.options import (
    get_new_user_options,
    get_pending_users_ids_by_options,
    remove_pending_user_options,
)
from bot.notifications.publisher import publish_notification
from bot.notifications.pending_users.counters import (
    get_pending_user_counter,
    update_pending_user_counter,
    remove_pending_user_counter,
)
from bot.notifications.schemas import Notification


async def on_new_user(message: IncomingMessage):
    async with message.process():
        json_data = json.loads(message.body.decode())
        
    new_user = NewUser(**json_data)
    options = get_new_user_options(new_user)
    users_ids = await get_pending_users_ids_by_options(options)
    print(users_ids)
    for user_id in users_ids:
        user_counter_value = await get_pending_user_counter(user_id)
        if user_counter_value != MAX_COUNTER_VALUE:
            await update_pending_user_counter(user_id)
            user_counter_value = await get_pending_user_counter(user_id)

        if user_counter_value == MAX_COUNTER_VALUE:
            notification = Notification(
                user_id=user_id, 
                text=NotificationText.new_users, 
                type=NotificationType.new_users,
            )
            await publish_notification(notification)
            await remove_pending_user_counter(user_id)
            await remove_pending_user_options(user_id)
            