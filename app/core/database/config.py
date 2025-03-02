from functools import cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from fastapi import Depends

from app.core.settings import get_settings

settings = get_settings()


@cache
def get_async_engine() -> AsyncEngine:
    return create_async_engine(
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_NAME}",
        pool_size=2
    )


@cache
def get_general_session_maker(
        general_engine: AsyncEngine = Depends(get_async_engine)
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=general_engine, autocommit=False, autoflush=False
    )


async def get_general_session(
        general_session_maker: async_sessionmaker[AsyncSession] = Depends(get_general_session_maker)
) -> AsyncGenerator[AsyncSession, None]:
    async with general_session_maker() as session:
        yield session
