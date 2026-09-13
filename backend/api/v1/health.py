from urllib.request import urlopen

from fastapi import APIRouter, Depends
from sqlalchemy import text

from backend.api.deps import get_db, require_admin
from backend.core.config import settings
from backend.core.db.models import User
from backend.libs.minio_client import get_minio_client
from backend.libs.redis_client import ping as redis_ping

router = APIRouter(tags=["monitoring"])


def check_http_endpoint(url: str) -> str:
    try:
        with urlopen(url, timeout=3) as response:
            return (
                "ok" if response.status == 200 else f"error: status {response.status}"
            )
    except (OSError, TimeoutError) as error:
        return f"error: {error}"


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/health/ready")
def readiness(db=Depends(get_db)) -> dict:
    checks = {}
    try:
        db.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception as e:
        checks["postgres"] = f"error: {e}"

    try:
        checks["redis"] = "ok" if redis_ping() else "error: ping failed"
    except Exception as e:
        checks["redis"] = f"error: {e}"

    try:
        get_minio_client().bucket_exists(settings.MINIO_BUCKET)
        checks["minio"] = "ok"
    except Exception as e:
        checks["minio"] = f"error: {e}"

    try:
        with urlopen(
            f"{settings.MLFLOW_TRACKING_URI.rstrip('/')}/health",
            timeout=3,
        ) as response:
            checks["mlflow"] = (
                "ok" if response.status == 200 else f"error: status {response.status}"
            )
    except Exception as e:
        checks["mlflow"] = f"error: {e}"

    overall = "ok" if all(v == "ok" for v in checks.values()) else "degraded"
    return {"status": overall, "checks": checks}


@router.get("/health/observability")
def observability_readiness() -> dict:
    checks = {
        "otel_collector": check_http_endpoint(settings.OTEL_COLLECTOR_HEALTH_URL),
        "prometheus": check_http_endpoint(
            f"{settings.PROMETHEUS_URL.rstrip('/')}/-/ready"
        ),
        "loki": check_http_endpoint(f"{settings.LOKI_URL.rstrip('/')}/ready"),
        "tempo": check_http_endpoint(f"{settings.TEMPO_URL.rstrip('/')}/ready"),
        "grafana": check_http_endpoint(
            f"{settings.GRAFANA_URL.rstrip('/')}/api/health"
        ),
    }
    overall = "ok" if all(value == "ok" for value in checks.values()) else "degraded"
    return {"status": overall, "checks": checks}


@router.get("/config")
def get_config(user: User = Depends(require_admin)) -> dict:
    data = settings.model_dump()
    for secret in (
        "JWT_SECRET_KEY",
        "POSTGRES_PASSWORD",
        "MINIO_SECRET_KEY",
        "LABEL_STUDIO_API_KEY",
        "ADMIN_PASSWORD",
    ):
        if secret in data:
            data[secret] = "***"
    return data
