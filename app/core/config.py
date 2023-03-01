import secrets
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = ''
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600
    # work version of database
    DATABASE_URL: str = 'postgresql+asyncpg://test_user:testtest@127.0.0.1:5432/test_db'

settings = Settings()