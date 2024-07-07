import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class BotConfig(BaseModel):
    TOKEN: str = os.getenv('BOT_TOKEN')
    ADMINS_IDS: str = list(map(int, os.getenv('ADMINS_IDS').split())) if os.getenv('ADMINS_IDS') else []
    MODERATOR_IDS: str = list(map(int, os.getenv('MODERATOR_IDS').split())) if os.getenv('MODERATOR_IDS') else []
    SUPPORT_ACCOUNT_USERNAME: str = os.getenv('SUPPORT_ACCOUNT_USERNAME')
    POINTS_FOR_BLOCKED_USER: str = os.getenv('BANNED_USER_AWARD', 50)
    GEOCODER_API_KEY: str = os.getenv('GEOCODER_API_KEY')
    GROUPS_AGES: dict = {
        'FIRST': [14, 15, 16, 17, 18],
        'SECOND': [19, 20, 21, 22, 23],
        'THIRD': [24, 25, 26, 27, 28]
    }


class DatabaseConfig(BaseModel):
    PORT: str = os.getenv('DB_PORT', '5432')
    HOST: str = os.getenv('DB_HOST')
    NAME: str = os.getenv('DB_NAME')
    USER: str = os.getenv('DB_USER')
    PASSWORD: str = os.getenv('DB_PASSWORD')

    URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"


class Settings(BaseModel):
    BOT: BotConfig = BotConfig()
    DATABASE: DatabaseConfig = DatabaseConfig()

    TEMPLATES_PATH: str = '../templates'
    MARKET_LINK: str = os.getenv('MARKET_LINK')


settings = Settings()
