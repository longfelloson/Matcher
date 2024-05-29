from typing import Optional

from aiogram.types import Message
from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: Optional[str]


class UserActions:
    REPORT = "report_user"
    CHANGE_CONFIG = "change_config"


class AdminActions:
    BLOCK = "block_user"


class UserStatuses:
    BLOCKED = "BLOCKED"
    ACTIVE = "ACTIVE"
    NOT_REGISTERED = "NOT_REGISTERED"


class UserGender:
    MALE = "MALE"
    FEMALE = "FEMALE"


class PreferredGender:
    MALE = "MALE"
    FEMALE = "FEMALE"
    BOTH = "BOTH"


class PreferredAgeGroup:
    FIRST = "FIRST"
    SECOND = "SECOND"
    THIRD = "THIRD"

    class Age:
        FIRST = "14 - 18"
        SECOND = "19 - 23"
        THIRD = "24 - 28"


def get_user_schema_from_message(message: Message) -> User:
    """

    """
    return User(
        user_id=message.from_user.id,
        username=message.from_user.username,
    )
