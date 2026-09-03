from backend.core.config import settings
from backend.libs.arq_pool import get_redis_settings
from backend.workers.tasks.train_token_classifier import (
    train_token_classifier,
)


class WorkerSettings:
    functions = [
        train_token_classifier,
    ]

    queue_name = settings.TRAINER_QUEUE_NAME
    redis_settings = get_redis_settings()

    max_jobs = 1
    job_timeout = settings.TRAINER_JOB_TIMEOUT_SECONDS
    keep_result = settings.TRAINER_RESULT_TTL_SECONDS

    allow_abort_jobs = True