from enum import StrEnum

from bot.users.registration.constants import MAX_AGE, MIN_AGE


class IncorrectInputAnswer(StrEnum):
    age = f"Введи возраст от {MIN_AGE} до {MAX_AGE} 😘"
    name = f"Это не похоже на имя 🤔"
    city = f"Используй только буквы 😘"
    buttons = "Используй кнопки 😘"
    photo = "Отправь фото 😘"


class WarningAnswer(StrEnum):
    turn_on_profile = "Сначала включи анкету в профиле 😘"
    blocked_user = "Ты был заблокирован в боте ⛔️"
    too_many_messages = "Слишком быстро, подождите секунду ⏳"
    user_can_send_message = "Ты снова можешь что-то отправить 😊"
    photo_is_uploading = "Фото загружается..."
