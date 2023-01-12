from functools import lru_cache

from pydantic import BaseSettings, SecretStr, Field


class RabbitMQSettings(BaseSettings):
    username: str = 'guest'
    password: SecretStr = 'guest'
    host: str = '127.0.0.1'
    port: int = 5672
    exchange: str = ''
    consumer_queue: str
    publisher_queue: str
    queue: str

    class Config:
        env_prefix = "RABBIT_"


class AuthSettings(BaseSettings):
    url: str = 'http://127.0.0.1:8000/api/fake/userinfo'
    authorization: str = 'BASIC fjdkjfdjkjdjfdkfdf434r543re=='


class ShortenerSettings(BaseSettings):
    endpoint: str = 'https://api-ssl.bitly.com/v4/shorten'
    token: SecretStr
    domain: str

    class Config:
        env_prefix = "SHORTENER_"


class Settings(BaseSettings):
    batch_size: int = Field(1000, env='BATCH_SIZE')
    rabbit: RabbitMQSettings = RabbitMQSettings()
    shortener: ShortenerSettings = ShortenerSettings()
    auth: AuthSettings = AuthSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
