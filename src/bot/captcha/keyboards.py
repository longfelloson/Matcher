from aiogram.utils.keyboard import (
    InlineKeyboardBuilder as InlineBuilder,
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
)


def captcha_keyboard(captcha: dict) -> InlineKeyboard:
    """
    Returns keyboard with buttons with emojis as captcha for user
    """
    buttons = [
        InlineButton(
            text=emoji,
            callback_data=f"select_captcha*{captcha[emoji]}"
        )
        for emoji in captcha
    ]
    return InlineBuilder().add(*buttons).as_markup()
