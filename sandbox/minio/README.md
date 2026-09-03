# MinIO Sandbox

Experimental MinIO (S3-compatible object storage) integration scripts.

## Scripts

- **upload.py** - Upload a file to MinIO bucket
- **download.py** - Download a file from MinIO bucket
- **list_versions.py** - List object versions (if versioning enabled)
- **enable_versioning.py** - Enable object versioning on a bucket

## How to use

```bash
# Upload a file
python sandbox/minio/upload.py

# Download a file
python sandbox/minio/download.py

# Enable versioning
python sandbox/minio/enable_versioning.py

# List versions
python sandbox/minio/list_versions.py
```

## Configuration

Set MinIO connection details in `.env` or edit scripts:
```
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=dev-bucket
```

## Notes

- These are sandbox/experimental scripts; use production code from `backend/`
- MinIO runs in Docker Compose; see `compose.yml`
- Bucket versioning is useful for data lineage and recovery
