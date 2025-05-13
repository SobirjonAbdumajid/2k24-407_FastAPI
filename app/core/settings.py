from functools import cache
import os
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

    # REDIS CREDENTIALS
    REDIS_HOST: str
    REDIS_PORT: str

    JWT_ENCRYPT_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_EXPIRE_SECONDS: int
    model_config = SettingsConfigDict(env_file=".env.test" if "PYTEST_CURRENT_TEST" in os.environ else ".env")

    @property
    def GET_POSTGRES_URL(self) -> str:
        return f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}'

    @property
    def GET_REDIS_URL(self) -> str:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0'


@cache
def get_settings() -> Settings:
    return Settings()
