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
from backend.workers.tasks.train_token_classifier import (
    train_token_classifier,
)

logger = get_logger("trainer-worker")


async def startup(ctx: dict) -> None:
    configure_telemetry(settings.OTEL_SERVICE_NAME)
    server, thread = start_worker_metrics_server(settings.TRAINER_METRICS_PORT)
    ctx["metrics_server"] = server
    ctx["metrics_thread"] = thread
    logger.info(
        "Trainer worker observability started on metrics port %s",
        settings.TRAINER_METRICS_PORT,
    )


async def shutdown(ctx: dict) -> None:
    stop_worker_metrics_server(ctx.get("metrics_server"))
    shutdown_telemetry()


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
    on_startup = startup
    on_shutdown = shutdown
