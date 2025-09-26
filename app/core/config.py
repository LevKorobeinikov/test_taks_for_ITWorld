from typing import Optional

from dotenv import load_dotenv
from pydantic import EmailStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'FastAPI Blog Backend'
    ENV: str = 'development'
    DEBUG: bool = True
    DATABASE_URL: str = 'sqlite+aiosqlite:///./dev.db'
    JWT_SECRET: str = 'change-me-secret'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080
    BCRYPT_ROUNDS: int = 12
    FIRST_SUPERUSER_EMAIL: Optional[EmailStr] = None
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None

    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8',
    }


settings = Settings()


def get_auth_data():
    return {
        'secret_key': settings.JWT_SECRET,
        'algorithm': settings.JWT_ALGORITHM,
    }
