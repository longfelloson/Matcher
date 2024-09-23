from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.messages.registration.enums.age import PreferredAgeGroupOption
from bot.messages.registration.enums.gender import GenderOption, PreferredGenderOption


def select_gender_keyboard() -> Keyboard:
    buttons = [
        Button(text=gender) for gender in GenderOption
    ]
    builder = Builder().row(
        *buttons
    )
    builder.row(
        Button(text="↩")
    )
    return builder.as_markup(resize_keyboard=True)


def select_preferred_gender_keyboard() -> Keyboard:
    buttons = [
        Button(text=preferred_gender) for preferred_gender in PreferredGenderOption
    ]
    builder = Builder().row(
        *buttons
    )
    builder.row(
        Button(text="↩")
    )
    return builder.as_markup(resize_keyboard=True, placeholder="Выбери пол, который хочешь оценивать")


def select_age_group_keyboard() -> Keyboard:
    """Клавиатура выбора группы поиска пользователей"""
    buttons = [
        Button(text=age_group) for age_group in PreferredAgeGroupOption
    ]
    builder = Builder().add(
        *buttons
    )
    builder.row(
        Button(text="↩")
    )
    return builder.as_markup(resize_keyboard=True)


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
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Введи название места, где ты живешь")


def back_button_keyboard() -> Keyboard:
    builder = Builder().row(
        Button(text="↩")
    )
    return builder.as_markup(resize_keyboard=True)
