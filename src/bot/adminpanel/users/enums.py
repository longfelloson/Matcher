from enum import StrEnum, auto


class Action(StrEnum):
    view_user = auto()
    view_users_amount = auto()
    block = auto()
    unblock = auto()


class ActionName(StrEnum):
    view_user = "Просмотреть пользователя"
    view_users_amount = "Просмотреть количество пользователей"
    block = "Заблокировать пользователя"
    unblock = "Разблокировать пользователя"
