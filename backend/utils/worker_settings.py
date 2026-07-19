from arq.connections import RedisSettings
from backend.core.config import settings


async def simple_work(ctx: dict, *args, **kwargs) -> dict:
    print(f"[simple_work] job_id={ctx.get('job_id')} args={args} kwargs={kwargs}")
    return {"job_id": ctx.get("job_id"), "args": args, "kwargs": kwargs}


class WorkerSettings:
    functions = [simple_work]
    redis_settings = RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT, database=settings.REDIS_DB)
    