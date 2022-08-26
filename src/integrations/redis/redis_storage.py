from typing import AsyncIterator

from aioredis import from_url, Redis


async def init_redis_pool() -> AsyncIterator[Redis]:
    session = from_url(
        "redis://redis:6379",
        encoding="utf-8",
        decode_responses=True
    )
    yield session
    await session.close()
