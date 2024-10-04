import random
from copy import deepcopy
from typing import Union

import emoji
from pycipher import Caesar

from bot.captcha.keyboards import captcha_keyboard
from bot.loader import bot

DEFAULT_CAPTCHA_EMOJIS_LIMIT = 5
EMOJIS = list(emoji.EMOJI_DATA.keys())

CIPHER = Caesar(key=3)


def generate_captcha(emojis_limit: int = DEFAULT_CAPTCHA_EMOJIS_LIMIT) -> dict:
    """Генерирует словарь с эмодзи и их верностью"""
    emojis_deep_copy = deepcopy(EMOJIS)
    random.shuffle(emojis_deep_copy)

    correct_emoji = random.choice(emojis_deep_copy[:emojis_limit])

    return {
        "correct_emoji": correct_emoji,
        "emojis": {
            emoji_: encrypt_correctness(emoji_, correct_emoji)
            for emoji_ in emojis_deep_copy[:emojis_limit]
        },
    }


def encrypt_correctness(emoji_: str, correct_emoji: str) -> str:
    def get_captcha_correctness():
        return "CORRECT" if emoji_ == correct_emoji else "NOT_CORRECT"

    encrypted_captcha_correctness = CIPHER.encipher(get_captcha_correctness())
    return encrypted_captcha_correctness


def decrypt_correctness(encrypted_captcha_correctness: str) -> str:
    return CIPHER.decipher(encrypted_captcha_correctness)


async def send_captcha(
        chat_id: Union[str, int],
        captcha_emojis: dict,
        hidden_correct_emoji: str
) -> None:
    await bot.send_message(
        chat_id=chat_id,
        text=f"Выберите эмодзи: {hidden_correct_emoji}",
        reply_markup=captcha_keyboard(captcha_emojis),
    )
