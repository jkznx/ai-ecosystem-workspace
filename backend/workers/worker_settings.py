from arq.connections import RedisSettings

from backend.core.config import settings
from backend.workers.tasks.simple_work import simple_work


class WorkerSettings:
    functions = [simple_work]
    redis_settings = RedisSettings(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, database=settings.REDIS_DB
    )