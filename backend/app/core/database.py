from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# convert sqlite url to async format for aiosqlite
# since fastapi uses asyncio, we need to use aiosqlite ( asych wrapper around sqlite)instead of sqlite3
SQLALCHEMY_DATABASE_URL = settings.database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
# create async database engine for sqlite
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {},
    echo=settings.debug
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()
# dependency function to get database session
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 