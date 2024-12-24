from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # PROJECT INFO
    PROJECT_NAME: str = 'PDP`s Hotel'
    PROJECT_DESCRIPTION: str = 'This is learning project'
    PROJECT_VERSION: str = '0.0.1'

    # POSTGRES CREDENTIALS
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    JWT_ENCRYPT_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_EXPIRE_SECONDS: int

    model_config = SettingsConfigDict(env_file='.env')


@cache
def get_settings() -> Settings:
    return Settings()
