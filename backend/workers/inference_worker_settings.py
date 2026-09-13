from backend.core.config import settings
from backend.core.logger import get_logger
from backend.libs.arq_pool import get_redis_settings
from backend.observability.metrics import (
    start_worker_metrics_server,
    stop_worker_metrics_server,
)
from backend.observability.telemetry import (
    configure_telemetry,
    shutdown_telemetry,
)
from backend.workers.tasks.predict_token_classifier import (
    predict_token_classification,
)

logger = get_logger("inference-worker")


async def startup(ctx: dict) -> None:
    configure_telemetry(settings.OTEL_SERVICE_NAME)
    server, thread = start_worker_metrics_server(settings.INFERENCE_METRICS_PORT)
    ctx["metrics_server"] = server
    ctx["metrics_thread"] = thread
    logger.info(
        "Inference worker observability started on metrics port %s",
        settings.INFERENCE_METRICS_PORT,
    )


async def shutdown(ctx: dict) -> None:
    stop_worker_metrics_server(ctx.get("metrics_server"))
    shutdown_telemetry()


class InferenceWorkerSettings:
    functions = [predict_token_classification]
    queue_name = settings.INFERENCE_QUEUE_NAME
    redis_settings = get_redis_settings()
    max_jobs = 1
    job_timeout = settings.INFERENCE_JOB_TIMEOUT_SECONDS
    keep_result = settings.INFERENCE_RESULT_TTL_SECONDS
    allow_abort_jobs = True
    on_startup = startup
    on_shutdown = shutdown
