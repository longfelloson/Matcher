from aiogram.types import Message, ReplyKeyboardMarkup

from bot.messages.schemas import Answers

MIN_USER_NAME_LENGTH = 3


def validate_age(text: str, min_age: int, max_age: int) -> bool:
    """
    Проверка пользовательского возраста
    """
    if not text.isdigit():
        return False
    return min_age <= int(text) <= max_age


def validate_user_name(text: str) -> bool:
    """
    Проверка пользовательского имени
    """
    if text.isdigit() or len(text) < MIN_USER_NAME_LENGTH:
        return False
    return True


async def validate_user_input(message: Message, keyboard: ReplyKeyboardMarkup):
    """
    Проверка пользовательского ввода, соответствует ли он кнопкам
    """
    rows = [row for row in keyboard.keyboard]
    buttons_texts = []

    for row in rows:
        for button in row:
            buttons_texts.append(button.text)

    if message.text in buttons_texts:
        return True
    await message.answer(Answers.INCORRECT_BUTTON_TEXT, reply_markup=keyboard)
