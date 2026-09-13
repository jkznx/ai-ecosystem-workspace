from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import select

from backend.api.v1 import api_v1_router
from backend.api.v1 import health as health_router_module
from backend.core.config import settings
from backend.core.db.models import User
from backend.core.db.session import Base, engine, get_session
from backend.core.exceptions import (
    AppError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)
from backend.core.logger import logger
from backend.core.security import hash_password
from backend.observability.metrics import prometheus_http_middleware
from backend.observability.telemetry import (
    configure_telemetry,
    shutdown_telemetry,
)

_STATUS_MAP = {
    NotFoundError: 404,
    ConflictError: 409,
    UnauthorizedError: 401,
    ForbiddenError: 403,
}


def _seed_admin() -> None:
    with get_session() as db:
        exists = db.scalar(select(User).where(User.username == settings.ADMIN_USERNAME))
        if exists is None:
            db.add(
                User(
                    username=settings.ADMIN_USERNAME,
                    hashed_password=hash_password(settings.ADMIN_PASSWORD),
                    is_admin=True,
                )
            )
            db.commit()
            logger.info("Seeded default admin user %r", settings.ADMIN_USERNAME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up %s", settings.APP_NAME)
    Base.metadata.create_all(bind=engine)
    _seed_admin()
    try:
        yield
    finally:
        logger.info("Shutting down %s", settings.APP_NAME)
        shutdown_telemetry()


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        """
    6610110428 Jukrachai Plongmai
    
    Backend API for AI Ecosystem Workspace.

    Provides APIs for authentication, students,
    storage, annotation and background jobs.
    """
    ),
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "auth", "description": "Login and Manage JWT token"},
        {"name": "minio", "description": "Object storage through MinIO"},
        {"name": "labelstudio", "description": "connect Label Studio"},
        {"name": "arq", "description": "Background job queue through ARQ/Redis"},
        {"name": "training", "description": "Scheduled GPU model training"},
        {"name": "inference", "description": "MLflow model inference through Redis"},
        {"name": "postgres", "description": "Data in PostgreSQL"},
        {"name": "monitoring", "description": "Health check and look config"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(prometheus_http_middleware)


@app.get(settings.PROMETHEUS_METRICS_PATH, include_in_schema=False)
def prometheus_metrics() -> Response:
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    status_code = _STATUS_MAP.get(type(exc), 400)
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


app.include_router(health_router_module.router)
app.include_router(api_v1_router)

configure_telemetry(
    settings.OTEL_SERVICE_NAME,
    app=app,
    sqlalchemy_engine=engine,
)
