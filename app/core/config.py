from pydantic import BaseSettings, Field

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'FastAPI Blog Backend'
    ENV: str = 'development'
    DEBUG: bool = True
    DATABASE_URL: str = Field(
        'sqlite+aiosqlite:///./dev.db', env='DATABASE_URL'
    )
    JWT_SECRET: str = Field('change-me-secret', env='JWT_SECRET')
    JWT_ALGORITHM: str = Field('HS256', env='JWT_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        15, env='ACCESS_TOKEN_EXPIRE_MINUTES'
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(
        60 * 24 * 7, env='REFRESH_TOKEN_EXPIRE_MINUTES'
    )
    BCRYPT_ROUNDS: int = Field(12, env='BCRYPT_ROUNDS')

    class Config:
        env_file = '.env'


settings = Settings()
