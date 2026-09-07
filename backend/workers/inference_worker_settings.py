from backend.core.config import settings
from backend.libs.arq_pool import get_redis_settings
from backend.workers.tasks.predict_token_classifier import (
    predict_token_classification,
)


class InferenceWorkerSettings:
    functions = [predict_token_classification]
    queue_name = settings.INFERENCE_QUEUE_NAME
    redis_settings = get_redis_settings()
    max_jobs = 1
    job_timeout = settings.INFERENCE_JOB_TIMEOUT_SECONDS
    keep_result = settings.INFERENCE_RESULT_TTL_SECONDS
    allow_abort_jobs = True
