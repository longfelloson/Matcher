from enum import StrEnum

from bot.users.registration.constants import MIN_AGE


class IncorrectInputAnswer(StrEnum):
    age = f"Твой возраст должен быть не меньше {MIN_AGE} лет 😘"
    name = f"Это не похоже на имя 🤔"
    city = f"Используй только буквы 😘"
    buttons = "Используй кнопки 😘"
    photo = "Отправь фото 😘"
