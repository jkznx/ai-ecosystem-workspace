import sys
from backend.utils.minio_client import get_minio_client, ensure_bucket


def download_file(object_name: str, output_path: str, version_id: str | None = None) -> None:
    bucket = ensure_bucket()
    client = get_minio_client()
    client.fget_object(bucket, object_name, output_path, version_id=version_id)
    print(f"Downloaded '{object_name}' [version_id={version_id or 'latest'}] -> '{output_path}'")


if __name__ == "__main__":
    ver = sys.argv[3] if len(sys.argv) > 3 else None
    download_file(sys.argv[1], sys.argv[2], ver)

