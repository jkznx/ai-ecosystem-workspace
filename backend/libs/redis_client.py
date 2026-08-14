import redis

from backend.core.config import settings


def get_redis_client() -> redis.Redis:
    return redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def ping() -> bool:
    client = get_redis_client()
    return bool(client.ping())