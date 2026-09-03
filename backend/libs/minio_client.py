from minio import Minio
from minio.error import S3Error

from backend.core.config import settings


def get_minio_client() -> Minio:
    return Minio(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
    )


def ensure_bucket(bucket_name: str) -> str:
    client = get_minio_client()

    if client.bucket_exists(bucket_name):
        return bucket_name

    try:
        client.make_bucket(bucket_name)
    except S3Error as error:
        if error.code not in {
            "BucketAlreadyExists",
            "BucketAlreadyOwnedByYou",
        }:
            raise

    return bucket_name