from pydantic import BaseModel

from bot.notifications.enums import NotificationText, NotificationType


class Notification(BaseModel):
    user_id: int | str
    text: NotificationText
    type: NotificationType
    