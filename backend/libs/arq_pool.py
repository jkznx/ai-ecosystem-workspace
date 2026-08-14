from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

from backend.core.config import settings


async def get_arq_pool() -> ArqRedis:
    return await create_pool(
        RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT, database=settings.REDIS_DB)
    )