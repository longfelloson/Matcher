from enum import StrEnum


class Answer(StrEnum):
    unknown_message = "Я не знаю эту команду 🤷‍♂️"
    blocked_user = "Ты заблокирован в боте!"
    incorrect_user_input = "Используй кнопки 😘"
    user_guesses_age = "Теперь ты угадываешь возраст 🔢"
    user_not_guesses_age = "Теперь ты только оцениваешь людей 🔎"


class ChangeProfileAnswer(StrEnum):
    change_name = "Отправь новое имя ⤵️"
    change_location = "Отправь локацию или город ⤵️"
    change_age = "Отправь новый возраст ⤵️"
    change_photo = "Отправь новое фото ⤵️"
    change_profile = "Выбери раздел, чтобы изменить его ⤵️"

    name_updated = "Имя обновлено ✅"
    photo_updated = "Фото обновлено ✅"
    age_updated = "Возраст обновлен ✅"
    location_updated = "Город обновлен ✅"
