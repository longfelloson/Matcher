from enum import StrEnum

from bot.users.enums.genders import UserGender
from bot.users.models import User


class RatesAnswer(StrEnum):
    answer_for_rater = "Ссылка на лайкнутого пользователя: {} 💞"
    someone_liked_you = "Кому-то понравилась ваша анкета 🥰"

    @staticmethod
    def get_answer_for_rated(rater: User, rater_link: str) -> str:
        verb = "оценил"
        if rater.gender == UserGender:
            verb += "a"

        return f"{rater_link} взаимно {verb} тебя, общайтесь 💞"
