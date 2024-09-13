import random
from copy import deepcopy

import emoji
from pycipher import Caesar

DEFAULT_CAPTCHA_EMOJIS_LIMIT = 5
EMOJIS = list(emoji.EMOJI_DATA.keys())

CIPHER = Caesar(key=3)


def generate_captcha(emojis_limit: int = DEFAULT_CAPTCHA_EMOJIS_LIMIT) -> dict:
    """Генерирует словарь с эмодзи и их верностью для капчи"""
    new_emojis = deepcopy(EMOJIS)
    random.shuffle(new_emojis)

    correct_emoji = random.choice(new_emojis[:emojis_limit])

    return {
        "correct_emoji": correct_emoji,
        "emojis": {
            emoji_: encrypt_correctness(emoji_, correct_emoji)
            for emoji_ in new_emojis[:emojis_limit]
        },
    }


def encrypt_correctness(emoji_: str, correct_emoji: str) -> str:
    def get_captcha_correctness():
        return "CORRECT" if emoji_ == correct_emoji else "NOT_CORRECT"

    encrypted_captcha_correctness = CIPHER.encipher(get_captcha_correctness())
    return encrypted_captcha_correctness


def decrypt_correctness(encrypted_captcha_correctness: str) -> str:
    return CIPHER.decipher(encrypted_captcha_correctness)
