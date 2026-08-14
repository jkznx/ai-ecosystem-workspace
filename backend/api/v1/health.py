from fastapi import APIRouter, Depends
from sqlalchemy import text

from backend.api.deps import get_db, require_admin
from backend.core.config import settings
from backend.core.db.models import User
from backend.libs.minio_client import get_minio_client
from backend.libs.redis_client import ping as redis_ping

router = APIRouter(tags=["monitoring"])


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

    overall = "ok" if all(v == "ok" for v in checks.values()) else "degraded"
    return {"status": overall, "checks": checks}


@router.get("/config")
def get_config(user: User = Depends(require_admin)) -> dict:
    data = settings.model_dump()
    for secret in ("JWT_SECRET_KEY", "POSTGRES_PASSWORD", "MINIO_SECRET_KEY", "LABEL_STUDIO_API_KEY", "ADMIN_PASSWORD"):
        if secret in data:
            data[secret] = "***"
    return data