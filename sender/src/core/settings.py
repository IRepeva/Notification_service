from functools import lru_cache

from pydantic import BaseSettings, SecretStr


class PostgresSettings(BaseSettings):
    user: str = 'postgres'
    password: str = 'password'
    host: str = 'localhost'
    port: int = 5432
    db: str = 'movies'

    class Config:
        env_prefix = "POSTGRES_"


class RabbitMQSettings(BaseSettings):
    username: str = 'guest'
    password: SecretStr = 'guest'
    host: str = '127.0.0.1'
    port: int = 5672
    exchange: str = ''
    queue: str = ''

    class Config:
        env_prefix = "RABBIT_"


class EmailServerSettings(BaseSettings):
    address: str
    port: int
    password: str
    login: str

    class Config:
        env_prefix = "EMAIL_"


class Settings(BaseSettings):
    rabbit: RabbitMQSettings = RabbitMQSettings()
    postgres: PostgresSettings = PostgresSettings()
    email: EmailServerSettings = EmailServerSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
