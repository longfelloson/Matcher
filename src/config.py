from typing import Union

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class S3Config(BaseSettings):
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT_URL: str
    S3_BUCKET_NAME: str


class RedisConfig(BaseSettings):
    REDIS_PORT: int = 6379
    REDIS_HOST: str
    REDIS_DB: int = 0

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class BotConfig(BaseSettings):
    BOT_TOKEN: str

    ADMINS_IDS: str
    MODERATOR_IDS: str

    SUPPORT_ACCOUNT_USERNAME: str
    POINTS_FOR_BLOCKED_USER: Union[int, float]
    GEOCODER_API_KEY: str

    @property
    def admins_ids(self):
        return list(map(int, self.ADMINS_IDS.split(",")))


class DatabaseConfig(BaseSettings):
    DB_PORT: int
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
    MARKET_EXCHANGE_RATE: Union[int, float]


class AuthConfig(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str


class PaymentsConfig(BaseSettings):
    PAYMENTS_BASE_URL: str
    PAYMENTS_PRIVATE_KEY: str
    PAYMENTS_PUBLIC_KEY: str
    PAYMENTS_ACCOUNT: str


class Settings(
    AuthConfig,
    S3Config,
    BotConfig,
    DatabaseConfig,
    MarketConfig,
    PaymentsConfig,
    RedisConfig,
):
    LOGS_FILE_PATH: str = Field(default="../errors.log")


settings = Settings()
