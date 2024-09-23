from enum import StrEnum


class UserStatus(StrEnum):
    reported = "reported"
    blocked = "blocked"
    active = "active"
    not_active = "not_active"
    left = "left"
