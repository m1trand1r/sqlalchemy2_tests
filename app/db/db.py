from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

url = 'postgresql+asyncpg://test_user:testtest@127.0.0.1:5432/test_db'

engine = create_async_engine(
    url=settings.DATABASE_URL,
    future=True,
    echo=True
)

AsyncSessionFactory = sessionmaker(
    engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)

async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session