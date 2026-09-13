from __future__ import annotations

from time import perf_counter
from typing import Any

from prometheus_client import Counter, Gauge, Histogram, start_http_server

from backend.core.config import settings

HTTP_REQUESTS = Counter(
    "ai_ecosystem_http_requests_total",
    "Total FastAPI HTTP requests.",
    ("method", "route", "status"),
)
HTTP_REQUEST_DURATION = Histogram(
    "ai_ecosystem_http_request_duration_seconds",
    "FastAPI request duration in seconds.",
    ("method", "route"),
)
HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "ai_ecosystem_http_requests_in_progress",
    "FastAPI requests currently being processed.",
    ("method",),
)
INFERENCE_JOBS = Counter(
    "ai_ecosystem_inference_jobs_total",
    "Inference jobs processed by the worker.",
    ("status", "model_name"),
)
INFERENCE_DURATION = Histogram(
    "ai_ecosystem_inference_job_duration_seconds",
    "Inference job duration in seconds.",
    ("model_name",),
)
INFERENCE_ENTITIES = Counter(
    "ai_ecosystem_inference_entities_total",
    "Entities produced by successful inference jobs.",
    ("model_name",),
)
TRAINING_JOBS = Counter(
    "ai_ecosystem_training_jobs_total",
    "Training jobs processed by the worker.",
    ("status", "model_name"),
)
TRAINING_DURATION = Histogram(
    "ai_ecosystem_training_job_duration_seconds",
    "Training job duration in seconds.",
    ("model_name",),
)


async def prometheus_http_middleware(request: Any, call_next: Any) -> Any:
    if request.url.path == settings.PROMETHEUS_METRICS_PATH:
        return await call_next(request)

    method = request.method
    started_at = perf_counter()
    status_code = 500
    HTTP_REQUESTS_IN_PROGRESS.labels(method=method).inc()

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        route = request.scope.get("route")
        route_path = getattr(route, "path", "unmatched")
        duration = perf_counter() - started_at
        HTTP_REQUESTS.labels(
            method=method,
            route=route_path,
            status=str(status_code),
        ).inc()
        HTTP_REQUEST_DURATION.labels(
            method=method,
            route=route_path,
        ).observe(duration)
        HTTP_REQUESTS_IN_PROGRESS.labels(method=method).dec()


def observe_inference_job(
    *,
    status: str,
    model_name: str,
    duration_seconds: float,
    entity_count: int = 0,
) -> None:
    INFERENCE_JOBS.labels(status=status, model_name=model_name).inc()
    INFERENCE_DURATION.labels(model_name=model_name).observe(duration_seconds)
    if entity_count:
        INFERENCE_ENTITIES.labels(model_name=model_name).inc(entity_count)


def observe_training_job(
    *,
    status: str,
    model_name: str,
    duration_seconds: float,
) -> None:
    TRAINING_JOBS.labels(status=status, model_name=model_name).inc()
    TRAINING_DURATION.labels(model_name=model_name).observe(duration_seconds)


def start_worker_metrics_server(port: int) -> tuple[Any, Any]:
    return start_http_server(port, addr="0.0.0.0")


def stop_worker_metrics_server(server: Any | None) -> None:
    if server is not None:
        server.shutdown()
        server.server_close()
