from typing import AsyncGenerator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import config

SQLALCHEMY_DATABASE_URL = config.get("SQLALCHEMY_DATABASE_URL")
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


async def get_session() -> AsyncGenerator:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.commit()
