import sys
from pathlib import Path
from backend.utils.minio_client import get_minio_client, ensure_bucket


def upload_file(local_path: str, object_name: str | None = None) -> str | None:
    bucket = ensure_bucket()
    client = get_minio_client()
    path = Path(local_path)
    object_name = object_name or path.name

    result = client.fput_object(bucket, object_name, str(path))
    print(f"Uploaded '{path}' -> object='{object_name}' etag={result.etag} version_id={result.version_id}")
    return result.version_id


if __name__ == "__main__":
    obj = sys.argv[2] if len(sys.argv) > 2 else None
    upload_file(sys.argv[1], obj)
