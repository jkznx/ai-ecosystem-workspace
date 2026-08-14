from fastapi import APIRouter

from backend.api.v1 import auth, health
from backend.api.v1.arq.router import router as arq_router
from backend.api.v1.labelstudio.router import router as labelstudio_router
from backend.api.v1.minio.router import router as minio_router
from backend.api.v1.postgres.router import router as postgres_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(minio_router)
api_v1_router.include_router(labelstudio_router)
api_v1_router.include_router(arq_router)
api_v1_router.include_router(postgres_router)
