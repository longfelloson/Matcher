from aiogram.utils.keyboard import (
    InlineKeyboardBuilder as InlineBuilder,
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
)


def captcha_keyboard(captcha_emojis: dict) -> InlineKeyboard:
    """Возвращает клавиатуру с кнопками с эмодзи"""
    buttons = [
        InlineButton(text=emoji, callback_data=f"select_captcha*{captcha_emojis[emoji]}")
        for emoji in captcha_emojis
    ]
    return InlineBuilder().add(*buttons).as_markup()
