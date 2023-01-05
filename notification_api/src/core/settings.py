from enum import Enum
from functools import lru_cache
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field, SecretStr

# LOGGING
logging_config.dictConfig(LOGGING)


class Queue(Enum):
    instant = True
    not_instant = False


class PostgresSettings(BaseSettings):
    user: str = 'postgres'
    password: str = 'password'
    host: str = 'localhost'
    port: int = 5432
    db: str = 'movies'

    @property
    def dsn(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'

    class Config:
        env_prefix = "POSTGRES_"


class RabbitMQSettings(BaseSettings):
    user_name: str = 'guest'
    password: SecretStr = 'guest'
    host: str = '127.0.0.1'
    port: int = 5672
    exchange: str = ''

    class Config:
        env_prefix = "RABBIT_"


class Settings(BaseSettings):
    project_name = Field('movies', env='PROJECT_NAME')
    rabbit: RabbitMQSettings = RabbitMQSettings()
    postgres: PostgresSettings = PostgresSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
