import os
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

GROUPS_AGES = {
    'FIRST': [14, 15, 16, 17, 18],
    'SECOND': [19, 20, 21, 22, 23],
    'THIRD': [24, 25, 26, 27, 28]
}

DATABASE_URL = os.getenv('DATABASE_URL')
ADMINS_IDS = list(map(int, os.getenv('ADMINS_IDS').split())) if os.getenv('ADMINS_IDS') else []
MODERATOR_IDS = list(map(int, os.getenv('MODERATOR_IDS').split())) if os.getenv('MODERATOR_IDS') else []
SUPPORT_ACCOUNT_USERNAME = os.getenv('SUPPORT_ACCOUNT_USERNAME')
POINTS_FOR_BLOCKED_USER = os.getenv('BANNED_USER_AWARD')
GEOCODER_API_KEY = os.getenv('GEOCODER_API_KEY')


def get_bot_info() -> Dict:
    """
    Получение информации о боте
    """
    return {
        'token': os.getenv('BOT_TOKEN'),
        'disable_web_page_preview': True,
        'parse_mode': 'HTML'
    }
