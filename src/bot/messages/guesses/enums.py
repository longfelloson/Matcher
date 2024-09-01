from enum import Enum
from typing import Union

from bot.users.enums import UserGender
from bot.users.models import User
from config import settings


class Answer(str, Enum):
    not_user_for_guess = "Нет пользователей для просмотра 🤷‍♂️"
    guess_age = "Угадай возраст ⤴️"
    rate_user = "Оцени пользователя ⤴️"

    @staticmethod
    def convert_score_to_currency(score: Union[int, float]) -> float:
        return score / settings.MARKET.MARKET_EXCHANGE_RATE

    @classmethod
    def get_age_guess_answer(
        cls,
        user: User,
        user_for_guess: User,
        score: Union[int, float],
    ) -> str:
        currency = cls.convert_score_to_currency(score)
        if score > 0:
            return (
                f"Ты получил {score} баллов (~{currency} ₽)  🎉"
                if user.gender == UserGender.male
                else f"Ты получила {score} баллов (~{currency} ₽)  🎉"
            )
        else:
            return (
                f"Ты не угадал, возраст анкеты - {user_for_guess.age} лет 🤷‍♂️"
                if user.gender == UserGender.male
                else f"Ты не угадала, возраст анкеты - {user_for_guess.age} лет 🤷‍♂️"
            )
