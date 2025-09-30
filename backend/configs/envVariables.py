from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    # Config API
    API_V1_STR: str
    BASE_URL: str

    # Config Banco de dados
    DB_URL: str
    DBBaseModel: ClassVar = declarative_base()

    # Config JWT
    JWT_SECRET: str
    ALGORITHM: str
    ACESS_TOKEN_EXPIRE_MINUTES: int

    # Config E-mail
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
