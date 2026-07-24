import sys
from backend.utils.minio_client import get_minio_client, ensure_bucket

def list_versions(object_name: str) -> None:
    bucket = ensure_bucket()
    client = get_minio_client()
    for obj in client.list_objects(bucket, prefix=object_name, include_version=True):
        if obj.object_name != object_name:
            continue
        latest = " (latest)" if obj.is_latest else ""
        print(f"version_id={obj.version_id} last_modified={obj.last_modified}{latest}")

if __name__ == "__main__":
    list_versions(sys.argv[1])
    
