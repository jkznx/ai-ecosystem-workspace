from minio.versioningconfig import VersioningConfig
from minio.commonconfig import ENABLED
from backend.utils.minio_client import get_minio_client, ensure_bucket

bucket = ensure_bucket()
client = get_minio_client()
client.set_bucket_versioning(bucket, VersioningConfig(ENABLED))
print(client.get_bucket_versioning(bucket).status) # Enabled