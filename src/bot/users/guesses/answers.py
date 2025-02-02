from enum import StrEnum

from bot.users.guesses.constants import SAME_AGE_GUESS_SCORE


class Answer(StrEnum):
    guess_age = "Угадай возраст ⤴️"
    rate_user = "Оцени пользователя ⤴️"

    @staticmethod
    def get_guess_answer(
        age: int, 
        age_suffix: str, 
        points: float,
    ) -> str:
        is_guess_correct = (
            True if points == SAME_AGE_GUESS_SCORE else False
        )
        answer = (
            f"Ты {'угадал' if is_guess_correct else 'не угадал'}, "
            f"возраст анкеты - {age} {age_suffix}"
        )
        if points:
            answer += f" (+{points} 🎈)"
        
        return answer
            