from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import RedirectResponse

from backend.api.deps import get_current_user
from backend.api.schemas.minio import StorageUploadResponse, StorageVersion
from backend.core.db.models import User
from backend.services.storage_service import storage_service

router = APIRouter(prefix="/minio", tags=["minio"])


# ---- store: write/update object ----
@router.post("/store/upload", response_model=StorageUploadResponse)
def upload(file: UploadFile, user: User = Depends(get_current_user)) -> StorageUploadResponse:
    result = storage_service.upload(file.filename, file.content_type, file.file)
    return StorageUploadResponse(**result)


@router.delete("/store/object/{object_name}", status_code=204)
def delete_object(object_name: str, version_id: str | None = None, user: User = Depends(get_current_user)) -> None:
    storage_service.delete(object_name, version_id=version_id)


# ---- load: read only ----
@router.get("/load/object/{object_name}")
def load_object(object_name: str, expires_minutes: int = 15, user: User = Depends(get_current_user)) -> RedirectResponse:
    url = storage_service.get_presigned_url(object_name, expires_minutes)
    return RedirectResponse(url)


@router.get("/load/versions/{object_name}", response_model=list[StorageVersion])
def load_versions(object_name: str, user: User = Depends(get_current_user)) -> list[StorageVersion]:
    return storage_service.list_versions(object_name)
