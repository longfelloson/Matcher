from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class S3Config(BaseSettings):
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT_URL: str
    S3_BUCKET_NAME: str


class BotConfig(BaseSettings):
    BOT_TOKEN: str

    CAPTCHA_ENCRYPTION_KEY: str

    ADMINS_IDS: str
    MODERATOR_IDS: str

    SUPPORT_ACCOUNT_USERNAME: str
    POINTS_FOR_BLOCKED_USER: str
    GEOCODER_API_KEY: str

    GROUPS_AGES: dict = {
        "FIRST": [14, 15, 16, 17, 18],
        "SECOND": [19, 20, 21, 22, 23],
        "THIRD": [24, 25, 26, 27, 28],
    }

    @property
    def admins_ids(self):
        return list(map(int, self.ADMINS_IDS.split(",")))


class DatabaseConfig(BaseSettings):
    DB_PORT: str
    DB_HOST: str
    DB_NAME: str
    DB_PASSWORD: str
    DB_USER: str

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class MarketConfig(BaseSettings):
    TEMPLATES_PATH: str = "../templates"
    MARKET_LINK: str
    MARKET_EXCHANGE_RATE: str


class AuthConfig(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str


class PaymentsConfig(BaseSettings):
    PAYMENTS_BASE_URL: str
    PAYMENTS_PRIVATE_KEY: str
    PAYMENTS_PUBLIC_KEY: str


class Settings:
    AUTH = AuthConfig()
    S3 = S3Config()
    BOT = BotConfig()
    DATABASE = DatabaseConfig()
    MARKET = MarketConfig()
    PAYMENTS = PaymentsConfig()


settings = Settings()
