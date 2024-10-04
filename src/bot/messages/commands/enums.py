from enum import StrEnum


class CommandAnswer(StrEnum):
    no_reported = "<b>Ты никого не просматриваешь 🤷‍♂️</b>\n\nИспользуй эту команду во время просмотра анкеты"
    start = "Привет 👋"
    help = "Нажми на кнопку ниже ⤵️"
    admin = "Панель управления ботом"
