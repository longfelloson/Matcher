import itertools

from aiogram.types import InlineKeyboardMarkup as InlineKeyboard, InlineKeyboardButton as InlineButton
from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.users.models import User
from bot.users.schemas import UserActions
from config import settings

GROUPS_AGES_BUTTONS = {
    'FIRST': [Button(text=str(age)) for age in settings.BOT.GROUPS_AGES['FIRST']],
    'SECOND': [Button(text=str(age)) for age in settings.BOT.GROUPS_AGES['SECOND']],
    'THIRD': [Button(text=str(age)) for age in settings.BOT.GROUPS_AGES['THIRD']]
}
ALL_GROUPS_AGES = list(map(str, itertools.chain.from_iterable(settings.BOT.GROUPS_AGES.values())))
USER_RATE_BUTTONS = ["❤", "👎"]
USER_GUESS_BUTTONS = ALL_GROUPS_AGES


def guess_user_age_keyboard(user: User) -> Keyboard:
    """
    Клавиатура с кнопками выбора возраста поиска анкет
    """
    builder = Builder().row(
        *GROUPS_AGES_BUTTONS[user.preferred_age_group]
    )
    builder.row(
        *[Button(text=text) for text in USER_RATE_BUTTONS]
    )
    return builder.row(Button(text='↩')).as_markup(resize_keyboard=True)


def report_keyboard(guesser: User, guessed: User) -> InlineKeyboard:
    """
    Клавиатура с кнопкой "Пожаловаться"
    """
    builder = Builder().row(
        InlineButton(
            text="⚠️",
            callback_data=f'{UserActions.REPORT}*{guesser.user_id}*{guessed.user_id}'
        )
    )
    return builder.as_markup()


def rate_user_keyboard() -> Keyboard:
    """
    Кнопки оценки пользователя
    """
    rate_user_buttons = [
        Button(text=text) for text in USER_RATE_BUTTONS
    ]
    builder = Builder().row(
        *rate_user_buttons
    )
    builder.row(
        Button(text='↩')
    )
    return builder.as_markup(resize_keyboard=True)
