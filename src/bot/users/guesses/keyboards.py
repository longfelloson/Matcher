import itertools

from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.users.registration.enums.age import AgeGroup

# Словарь с кнопками возрастов групп
AGE_GROUPS_BUTTONS = {
    group.name: [
        Button(text=str(age)) for age in group.ages
    ]
    for group in AgeGroup
}

# Список со всеми возрастами со всех возрастных групп
ALL_AGE_GROUPS = list(map(str, itertools.chain.from_iterable([group.ages for group in AgeGroup])))

USER_RATE_BUTTONS = ["❤", "👎"]
USER_GUESS_BUTTONS = ALL_AGE_GROUPS


def guess_user_age_keyboard(age_group_name: str) -> Keyboard:
    """Клавиатура с кнопками выбора возраста поиска анкет"""
    builder = Builder().row(
        *AGE_GROUPS_BUTTONS[age_group_name]
    )
    return builder.row(Button(text="↩")).as_markup(resize_keyboard=True)


def rate_user_keyboard() -> Keyboard:
    """Кнопки оценки пользователя"""
    rate_user_buttons = [
        Button(text=text) for text in USER_RATE_BUTTONS
    ]
    builder = Builder().row(
        *rate_user_buttons
    )
    builder.row(
        Button(text="↩")
    )
    return builder.as_markup(resize_keyboard=True)
