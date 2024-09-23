from enum import StrEnum


class Answer(StrEnum):
    unknown_message = "Я не знаю эту команду 🤷‍♂️"
    blocked_user = "Ты заблокирован в боте!"
    incorrect_user_input = "Используй кнопки 😘"
    user_guesses_age = "Теперь ты угадываешь возраст 🔢"
    user_not_guesses_age = "Теперь ты только оцениваешь людей 🔎"


class ChangeProfileAnswer(StrEnum):
    name = "Отправь новое имя ⤵️"
    location = "Отправь локацию или город ⤵️"
    age = "Отправь новый возраст ⤵️"
    photo = "Отправь новое фото ⤵️"
    profile = "Выбери раздел, чтобы изменить его ⤵️"
    gender = "Выбери свой пол ⤵️"
    preferred_gender = "Кого будешь просматривать ⤵️"
    viewer_gender = "Кто будет просматривать тебя ⤵️"


class UpdatedProfileAnswer(StrEnum):
    name = "Имя обновлено ✅"
    photo = "Фото обновлено ✅"
    age = "Возраст обновлен ✅"
    location = "Город обновлен ✅"
    gender = "Пол обновлен ✅"
    preferred_gender = "Теперь ты ищешь другой пол ✅"
    viewer_gender = "Теперь тебя просматривает другой пол ✅"
