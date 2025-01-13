from enum import StrEnum

from bot.users.enums.genders import UserViewerGender
from bot.users.registration.enums.gender import PreferredGender


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

    @staticmethod
    def get_preffered_gender_answer(gender: PreferredGender):
        match gender:
            case PreferredGender.male:
                return "Теперь ты просматриваешь парней ✅"
            case PreferredGender.female:
                return "Теперь ты просматриваешь девушек ✅"
            case PreferredGender.both:
                return "Теперь ты просматриваешь любой пол ✅"

    @staticmethod
    def get_viewer_gender_answer(gender: UserViewerGender):
        match gender:
            case UserViewerGender.male:
                return "Теперь тебя просматривают парни ✅"
            case UserViewerGender.female:
                return "Теперь тебя просматривают девушки ✅"
            case UserViewerGender.both:
                return "Теперь тебя просматривают и девушки, и парни ✅"
