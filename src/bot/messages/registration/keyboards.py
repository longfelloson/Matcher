from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.users.enums import PreferredAgeGroup


def select_gender_keyboard() -> Keyboard:
    builder = Builder().row(
        Button(text="Парень"),
        Button(text="Девушка")
    )
    builder.row(
        Button(text="↩")
    )
    return builder.as_markup(resize_keyboard=True, single_use=True)


def select_preferred_gender_keyboard() -> Keyboard:
    """Клавиатура выбора пола анкет для поиска"""
    builder = Builder().row(
        Button(text="Парней"),
        Button(text="Девушек"),
    )
    builder.row(
        Button(text="↩")
    )
    return builder.as_markup(
        resize_keyboard=True,
        single_use=True,
        placeholder="Выбери пол, который хочешь оценивать",
    )


def select_age_group_keyboard() -> Keyboard:
    """
    Клавиатура выбора группы поиска пользователей
    """
    builder = Builder().add(
        Button(text=PreferredAgeGroup.Age.first),
        Button(text=PreferredAgeGroup.Age.second),
        Button(text=PreferredAgeGroup.Age.third),
    )
    builder.row(
        Button(text="↩")
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def select_location_keyboard() -> Keyboard:
    builder = Builder().row(
        Button(text="Москва"),
        Button(text="Санкт-Петербург")
    )
    builder.row(
        Button(text="🗺 Отправить свое место", request_location=True)
    )
    builder.row(
        Button(text="↩")
    )
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Введи название места, где ты живешь",
    )


def back_button_keyboard() -> Keyboard:
    builder = Builder().row(
        Button(text="↩")
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
