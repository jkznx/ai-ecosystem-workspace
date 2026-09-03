from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

from backend.core.config import settings


def get_redis_settings() -> RedisSettings:
    return RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        database=settings.REDIS_DB,
    )


async def get_arq_pool() -> ArqRedis:
    return await create_pool(get_redis_settings())