from typing import Any
from pydantic import BaseModel


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