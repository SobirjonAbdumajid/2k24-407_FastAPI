import redis

from app.core.settings import get_settings

settings = get_settings()


async def get_redis_client():
    return redis.asyncio.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )


async def get_redis_session():
    async with get_redis_client() as client:
        yield client
