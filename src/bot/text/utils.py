from bot.users.models import User


def get_profile_text(user: User) -> str:
    """
    Текст анкеты пользователя в его профиле
    """
    return (
        f"🎫 Имя: {bold(user.name)}\n\n"
        f"🎈 Баллов: {bold(int(user.points))}\n\n"
        f"🔢 Возраст: {bold(user.age)}\n\n"
        f"🌆 Город: {bold(user.city)}"
    )


def get_user_profile_caption(rater: User, rated: User) -> str:
    """
    Возвращает описание профиля пользовательской анкеты при просмотре другим пользователем
    """
    base_caption = f"{rated.name}, {rated.city}"

    if rater.instagram:
        base_caption += f", Instagram: <code>{rated.instagram}</code>"

    if not rater.config.guess_age:
        base_caption += f", {rater.age} лет"

    return base_caption


def bold(text: str) -> str:
    return f"<b>{text}</b>"
