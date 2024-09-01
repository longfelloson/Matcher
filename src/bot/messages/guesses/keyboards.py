import itertools

from aiogram.types import (
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
)
from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.users.enums import (
    UserAction,
    AgeGroup,
)
from bot.users.models import User


# Словарь с кнопками возрастов групп
AGE_GROUPS_BUTTONS = {
    group: [
        Button(text=str(age)) for age in group.ages
    ]
    for group in AgeGroup
}

# Список со всеми возрастами со всех возрастных групп
ALL_AGE_GROUPS = list(map(str, itertools.chain.from_iterable([group.ages for group in AgeGroup])))

USER_RATE_BUTTONS = ["❤", "👎"]
USER_GUESS_BUTTONS = ALL_AGE_GROUPS


def guess_user_age_keyboard(age_group: AgeGroup) -> Keyboard:
    """Клавиатура с кнопками выбора возраста поиска анкет"""
    builder = Builder().row(
        *AGE_GROUPS_BUTTONS[age_group]
    )
    builder.row(
        *[Button(text=text) for text in USER_RATE_BUTTONS]
    )
    return builder.row(Button(text="↩")).as_markup(resize_keyboard=True)


def report_keyboard(guesser: User, guessed: User) -> InlineKeyboard:
    builder = Builder().row(
        InlineButton(
            text="⚠️",
            callback_data=f"{UserAction.report_user}*{guesser.user_id}*{guessed.user_id}",
        )
    )
    return builder.as_markup()


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
