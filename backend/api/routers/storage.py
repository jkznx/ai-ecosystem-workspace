from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from minio.error import S3Error

from backend.api.deps import get_current_user
from backend.api.schemas import StorageUploadResponse, StorageVersion
from backend.core.db.models import User
from backend.utils.minio_client import get_minio_client, ensure_bucket

router = APIRouter(prefix="/storage", tags=["storage"])

@router.post("/upload", response_model=StorageUploadResponse)
def upload(file: UploadFile, user: User = Depends(get_current_user)) -> StorageUploadResponse:
    bucket = ensure_bucket()
    client = get_minio_client()
    result = client.put_object(
        bucket, file.filename, file.file, length=-1, part_size=10 * 1024 * 1024,
        content_type=file.content_type or "application/octet-stream",
    )
    return StorageUploadResponse(object_name=file.filename, etag=result.etag, version_id=result.version_id)

@router.get("/{object_name}")
def download(object_name: str, expires_minutes: int = 15, user: User = Depends(get_current_user)) -> RedirectResponse:
    bucket = ensure_bucket()
    client = get_minio_client()
    try:
        url = client.presigned_get_object(bucket, object_name, expires=timedelta(minutes=expires_minutes))
    except S3Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    return RedirectResponse(url)

@router.get("/{object_name}/versions", response_model=list[StorageVersion])
def list_versions(object_name: str, user: User = Depends(get_current_user)) -> list[StorageVersion]:
    bucket = ensure_bucket()
    client = get_minio_client()
    return [
        StorageVersion(
            version_id=obj.version_id,
            last_modified=obj.last_modified.isoformat() if obj.last_modified else None,
            is_latest=bool(obj.is_latest),
        )
        for obj in client.list_objects(bucket, prefix=object_name, include_version=True)
        if obj.object_name == object_name
    ]

@router.delete("/{object_name}", status_code=204)
def delete_object(object_name: str, version_id: str | None = None, user: User = Depends(get_current_user)) -> None:
    bucket = ensure_bucket()
    client = get_minio_client()
    client.remove_object(bucket, object_name, version_id=version_id)