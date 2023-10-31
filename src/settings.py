import logging
import os
import secrets
from pathlib import Path

from pydantic import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    PROJECT_NAME: str
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_RELOAD: bool = False
    ALLOW_ORIGINS: list = ["*"]

    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DATABASE_URL: str
    ECHO_SQL: bool = False

    LOG_LEVEL: str = "INFO"
    LOG_DESTINATIONS: list = ["console"]

    UVICORN_ACCESS_LOG_LEVEL: str = "INFO"
    UVICORN_ERROR_LOG_LEVEL: str = "INFO"
    UVICORN_LOG_HANDLERS: list = ["console"]

    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_EMAIL: str

    INIT_DB_IF_NOT_INITIALIZED: bool = False

    class Config:
        try:
            env = os.environ["APP_ENV"]
        except KeyError:
            env = "development"
        logger.warning("Loading `%s` environment", env)
        env_file = Path(__file__).parent / f"config/{env}.env"
        case_sensitive = True


settings = Settings()  # pylint: disable=invalid-name
