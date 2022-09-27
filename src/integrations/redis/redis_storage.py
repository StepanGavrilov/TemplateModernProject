from typing import AsyncIterator

from aioredis import from_url, Redis
from config import config


async def init_redis_pool() -> AsyncIterator[Redis]:
    session = from_url(
        f"redis://{config.get('REDIS_HOST', 'redis')}:6379",
        encoding="utf-8",
        decode_responses=True
    )
    yield session
    await session.close()
