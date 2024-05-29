import itertools

from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup as InlineKeyboard, InlineKeyboardButton as InlineButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder


from src import config
from src.users.models import User
from src.users.schemas import UserActions

GROUPS_AGES_BUTTONS = {
    'FIRST': [Button(text=str(age)) for age in config.GROUPS_AGES['FIRST']],
    'SECOND': [Button(text=str(age)) for age in config.GROUPS_AGES['SECOND']],
    'THIRD': [Button(text=str(age)) for age in config.GROUPS_AGES['THIRD']]
}
ALL_GROUPS_AGES = list(map(str, itertools.chain.from_iterable(config.GROUPS_AGES.values())))
USER_RATE_BUTTONS = ["❤", "👎"]
USER_GUESS_BUTTONS = ALL_GROUPS_AGES


def guess_user_age_keyboard(user: User) -> Keyboard:
    """

    """
    builder = Builder().row(*GROUPS_AGES_BUTTONS[user.preferred_age_group])
    builder.row(*[Button(text=text) for text in USER_RATE_BUTTONS])
    return builder.row(Button(text='↩')).as_markup(resize_keyboard=True)


def report_keyboard(guesser: User, guessed: User) -> InlineKeyboard:
    """
    Клавиатура с кнопкой "Пожаловаться"
    """
    return InlineKeyboard(inline_keyboard=[[InlineButton(
        text="⚠️",
        callback_data=f'{UserActions.REPORT}*{guesser.user_id}*{guessed.user_id}'
    )]])


def rate_user_keyboard() -> Keyboard:
    """

    """
    builder = Builder().row(*[Button(text=text) for text in USER_RATE_BUTTONS])
    builder.row(Button(text='↩'))
    return builder.as_markup(resize_keyboard=True)
