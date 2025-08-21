from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str  = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://meu_usuario:senha123@localhost:5432/deteccao"
    DBBaseModel: ClassVar = declarative_base() 

    JWT_SECRET: str = 'segredo-trocar'
    ALGORITHM: str = 'HS256'
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    model_config = SettingsConfigDict(
        env_file='.env',        # arquivo .env que será lido
        case_sensitive=True     # diferencia maiúsculas e minúsculas
    )


settings = Settings()
