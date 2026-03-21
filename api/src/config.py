from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_NAME: str = "Template"
    APP_ID: str = "template"
    DEBUG: bool = False
    DB_URL: str


@lru_cache
def get_config() -> Config:
    return Config()  # type: ignore[call-arg]
