from pydantic import BaseModel


class StorageUploadResponse(BaseModel):
    object_name: str
    etag: str
    version_id: str | None = None


class StorageVersion(BaseModel):
    version_id: str | None
    last_modified: str | None
    is_latest: bool