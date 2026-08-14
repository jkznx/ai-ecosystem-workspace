from datetime import timedelta
from typing import BinaryIO

from minio.error import S3Error

from backend.core.exceptions import NotFoundError
from backend.libs.minio_client import ensure_bucket, get_minio_client


class StorageService:
    """Business logic รอบ MinIO: ไม่รู้จัก FastAPI, เทสได้ตรง ๆ โดยไม่ต้อง mock request."""

    def upload(self, filename: str, content_type: str | None, stream: BinaryIO) -> dict:
        bucket = ensure_bucket()
        client = get_minio_client()
        result = client.put_object(
            bucket, filename, stream, length=-1, part_size=10 * 1024 * 1024,
            content_type=content_type or "application/octet-stream",
        )
        return {"object_name": filename, "etag": result.etag, "version_id": result.version_id}

    def get_presigned_url(self, object_name: str, expires_minutes: int = 15) -> str:
        bucket = ensure_bucket()
        client = get_minio_client()
        try:
            return client.presigned_get_object(bucket, object_name, expires=timedelta(minutes=expires_minutes))
        except S3Error as e:
            raise NotFoundError(f"object '{object_name}' not found") from e

    def list_versions(self, object_name: str) -> list[dict]:
        bucket = ensure_bucket()
        client = get_minio_client()
        return [
            {
                "version_id": obj.version_id,
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
                "is_latest": bool(obj.is_latest),
            }
            for obj in client.list_objects(bucket, prefix=object_name, include_version=True)
            if obj.object_name == object_name
        ]

    def delete(self, object_name: str, version_id: str | None = None) -> None:
        bucket = ensure_bucket()
        client = get_minio_client()
        client.remove_object(bucket, object_name, version_id=version_id)


storage_service = StorageService()
