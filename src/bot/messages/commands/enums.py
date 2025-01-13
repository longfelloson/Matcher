from enum import StrEnum

from bot.texts.utils import bold


class CommandAnswer(StrEnum):
    no_reported = (
        f"{bold('Ты никого не просматриваешь 🤷‍♂️</b>')}\n\n"
        "Используй эту команду во время просмотра анкеты"
    )
    start = "Привет 👋"
    help = "Нажми на кнопку ниже ⤵️"
    admin = "Панель управления ботом"
