from bot.users.models import User


class Answer:
    not_user_for_guess = "Нет пользователей для просмотра 🤷‍♂️"
    guess_age = "Угадай возраст ⤴️"
    rate_user = "Оцени пользователя ⤴️"

    @staticmethod
    def get_age_guess_answer(
            user: User, user_for_guess: User, score: int | float
    ) -> str:
        if score > 0:
            return (
                f"Ты получил {score} баллов 🎉"
                if user.gender == "MALE"
                else f"Ты получила {score} баллов 🎉"
            )
        else:
            answer_for_male = (
                f"Ты не угадал, возраст анкеты - {user_for_guess.age} лет 🤷‍♂️"
            )
            answer_for_female = (
                f"Ты не угадала, возраст анкеты - {user_for_guess.age} лет 🤷‍♂️"
            )
            return answer_for_male if user.gender == "MALE" else answer_for_female
