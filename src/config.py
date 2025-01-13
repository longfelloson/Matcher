from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_HOST = "redis"
DEFAULT_REDIS_DB = 0

DEFAULT_LOGS_PATH = "../errors.log"


class S3Config(BaseSettings):
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT_URL: str
    S3_BUCKET_NAME: str


class RedisConfig(BaseSettings):
    REDIS_PORT: int = DEFAULT_REDIS_PORT
    REDIS_HOST: str = DEFAULT_REDIS_HOST
    REDIS_DB: int = DEFAULT_REDIS_DB

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class BotConfig(BaseSettings):
    BOT_TOKEN: str

    ADMINS_IDS: str
    MODERATOR_IDS: str

    SUPPORT_ACCOUNT_USERNAME: str
    POINTS_FOR_BLOCKED_USER: int | float
    GEOCODER_API_KEY: str

    @property
    def moderators_ids(self):
        return list(map(int, self.MODERATOR_IDS.split(",")))

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
    MARKET_EXCHANGE_RATE: int | float


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
    LOGS_FILE_PATH: str = DEFAULT_LOGS_PATH


settings = Settings()
