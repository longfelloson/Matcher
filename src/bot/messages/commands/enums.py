from enum import Enum


class CommandAnswer(str, Enum):
    no_reported = "<b>Ты никого не просматриваешь 🤷‍♂️</b>\n\nИспользуй эту команду во время просмотра анкеты"
    report = "Жалоба отправлена 📨"
    start = "Привет 👋"
    help = "Нажми на кнопку ниже ⤵️"
    admin = "Панель управления ботом"
