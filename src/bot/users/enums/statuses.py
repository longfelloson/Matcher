from enum import StrEnum


class UserStatus(StrEnum):
    reported = "reported"
    blocked = "blocked"
    active = "active"
    inactive = "inactive"
    left = "left"
