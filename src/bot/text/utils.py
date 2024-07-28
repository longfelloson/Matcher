from bot.users.models import User


def get_profile_text(user: User) -> str:
    """
    Returns user's formatted profile text
    """
    return f"🎫 Имя: {bold(user.name)}\n\n" \
           f"🎈 Баллов: {bold(int(user.points))}\n\n" \
           f"🔢 Возраст: {bold(user.age)}\n\n" \
           f"🌆 Город: {bold(user.city)}"


def get_user_profile_caption(rater: User, rated: User) -> str:
    """
    Returns formatted user's caption of user's photo
    """
    base_caption = f"{rated.name}, {rated.city}"

    if rater.instagram:
        base_caption += f", Instagram: <code>{rated.instagram}</code>"

    if not rater.config.guess_age:
        base_caption += f", {rater.age} лет"

    return base_caption


def bold(text: str) -> str:
    return f"<b>{text}</b>"
