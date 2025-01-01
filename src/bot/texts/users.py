from bot.texts.utils import bold
from bot.users.guesses.answers import Answer
from bot.users.models import User


def get_age_suffix(age):
    if not isinstance(age, int) or age < 0:
        raise ValueError('Возраст должен быть неотрицательным целым числом.')

    last_digit = age % 10
    last_two_digits = age % 100

    if 11 <= last_two_digits <= 14:
        return 'лет'
    elif last_digit == 1:
        return 'год'
    elif last_digit in {2, 3, 4}:
        return 'года'
    else:
        return 'лет'


def get_profile_text(user: User) -> str:
    """Текст анкеты пользователя в его профиле"""
    currency = Answer.convert_score_to_currency(user.points)
    points_info = f"{int(user.points)} (~{currency} ₽)"
    return (
        f"👤 Имя: {bold(user.name)}\n\n"
        f"🎈 Баллов: {bold(points_info)}\n\n"
        f"🔢 Возраст: {bold(user.age)}\n\n"
        f"🌃 Город: {bold(user.city)}"
    )


def get_user_profile_caption(viewer: User, viewed: User) -> str:
    """Возвращает описание профиля пользовательской анкеты при просмотре другим пользователем"""
    base_caption = f"{viewed.name}, {viewed.city}"

    if viewed.instagram:
        base_caption += f", Instagram: <code>{viewed.instagram}</code>"

    if not viewer.config.guess_age:
        age_suffix = get_age_suffix(viewed.age)
        base_caption += f", {viewed.age} {age_suffix}"

    return base_caption


def get_user_link(user: User) -> str:
    return f"@{user.username}" if user.username else f'<a href="tg://user?id={user.user_id}">{user.name}</a>'
