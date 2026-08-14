import asyncio
from arq import create_pool
from arq.connections import RedisSettings
from backend.core.config import settings


async def main() -> None:
    redis = await create_pool(RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT, database=settings.REDIS_DB))
    job = await redis.enqueue_job("simple_work", "hello", student="Alice", major="CS")
    print(f"Enqueued job: {job.job_id}")
    print(f"Result: {await job.result(timeout=10)}")


if __name__ == "__main__":
    asyncio.run(main())