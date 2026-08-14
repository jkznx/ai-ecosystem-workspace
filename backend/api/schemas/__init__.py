from typing import Any
from pydantic import BaseModel, ConfigDict, EmailStr
from backend.api.schemas.auth import Token, UserRead
from backend.api.schemas.minio import StorageUploadResponse
from backend.api.schemas.arq import JobEnqueueRequest
from backend.api.schemas.labelstudio import LabelStudioProject
from backend.api.schemas.postgres import StudentRead

class StudentBase(BaseModel):
    name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    is_admin: bool

class Page(BaseModel):
    items: list[Any]
    total: int
    skip: int
    limit: int

class JobEnqueueRequest(BaseModel):
    function: str
    args: list[Any] = []
    kwargs: dict[str, Any] = {}

class JobEnqueueResponse(BaseModel):
    job_id: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: object | None = None

class StorageUploadResponse(BaseModel):
    object_name: str
    etag: str
    version_id: str | None = None

class StorageVersion(BaseModel):
    version_id: str | None
    last_modified: str | None
    is_latest: bool