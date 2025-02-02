from enum import StrEnum

from bot.notifications.pending_users.constants import MAX_COUNTER_VALUE


class NotificationText(StrEnum):
    new_users = (
        f"Найдено {MAX_COUNTER_VALUE} новых пользователей для просмотра 🔎"
    )
    

class NotificationType(StrEnum):
    new_users = "new_users"
