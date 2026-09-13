# MinIO (Object Storage) API

Endpoints for S3-compatible object storage via MinIO.

## Endpoints

- `GET /v1/minio/buckets` - List buckets
- `GET /v1/minio/buckets/{bucket}/objects` - List objects in bucket
- `POST /v1/minio/buckets/{bucket}/upload` - Upload object
- `GET /v1/minio/buckets/{bucket}/objects/{object_name}/download` - Download object
- `DELETE /v1/minio/buckets/{bucket}/objects/{object_name}` - Delete object

## How to use

```bash
# List buckets
curl http://localhost:8000/v1/minio/buckets

# Upload file
curl -X POST -F "file=@data.csv" \
  http://localhost:8000/v1/minio/buckets/my-bucket/upload
```

## Configuration

Set MinIO connection details in `.env`:
```
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

## Client

MinIO client is initialized in `backend/libs/minio_client.py`.
