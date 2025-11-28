from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# 本番/開発用のDB URL (テスト時はこれを上書きします)
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/main_db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


# Dependency Injection用関数
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
