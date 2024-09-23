from enum import StrEnum
from typing import Union

from config import settings


class Answer(StrEnum):
    not_user_for_guess = "Нет пользователей для просмотра 🤷‍♂️"
    guess_age = "Угадай возраст ⤴️"
    rate_user = "Оцени пользователя ⤴️"

    @staticmethod
    def convert_score_to_currency(score: Union[int, float]) -> float:
        return score / settings.MARKET_EXCHANGE_RATE
