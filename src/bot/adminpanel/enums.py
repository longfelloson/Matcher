from enum import StrEnum, auto


class Section(StrEnum):
    users = auto()
    stats = auto()


class SectionName(StrEnum):
    users = "Пользователи"
    stats = "Статистика"
