from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = ''
    SECRET_KEY: str = 'KISyDiqYCPdICd1IKExrioSWKXulieOpWXT4xYonw7R7ikvsaTdG7KlJj84vSrUpwXgCFM23mrL5sBHGyMrTPw'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*60
    # work version of database
    DATABASE_URL: str = 'postgresql+asyncpg://test_user:testtest@127.0.0.1:5432/test_db'

settings = Settings()