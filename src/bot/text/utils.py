from bot.users.models import User


def get_profile_text(user: User, points: int | float) -> str:
    """
    Returns user's formatted profile text
    """
    return f"🎫 Имя: {bold(user.name)}\n\n" \
           f"🎈 Баллов: {bold(points)}\n\n" \
           f"🔢 Возраст: {bold(user.age)}\n\n" \
           f"🌆 Город: {bold(user.city)}"


def get_user_profile_caption(user: User) -> str:
    """
    Returns formatted user's caption of user's photo
    """
    base_caption = f"{user.name}, {user.city}"

    if user.instagram:
        base_caption += f", Instagram: <code>{user.instagram}</code>"

    if not user.config.guess_age:
        base_caption += f", "

    return base_caption


def bold(text: str) -> str:
    return f"<b>{text}</b>"
