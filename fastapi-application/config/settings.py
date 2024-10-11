from typing import Literal

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class GunicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    timeout: int = 900


class LoggingConfig(BaseModel):
    log_level: Literal[
        'debug',
        'info',
        'warning',
        'error',
        'critical',
    ] = 'info'
    log_format: str = LOG_DEFAULT_FORMAT


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    user: str = "/user"
    auth: str = "/auth"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthUserConfig(BaseModel):
    algorithm: str = "HS256"
    secret_key: str = "secreT_passworD+"
    expire_access_token: float = 900.0  # 900 seconds = 15 minutes
    expire_refresh_token: float = 604_800.0  # 604800 seconds = 7 days


class MailConfig(BaseModel):
    m_from: str
    m_port: str
    m_server: str
    m_username: str
    m_password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    mail: MailConfig
    db: DatabaseConfig

    api: ApiPrefix = ApiPrefix()
    run: RunConfig = RunConfig()
    logging: LoggingConfig = LoggingConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    auth_user: AuthUserConfig = AuthUserConfig()

    secret_key: str = "secreT_passworD"


settings = Settings()
