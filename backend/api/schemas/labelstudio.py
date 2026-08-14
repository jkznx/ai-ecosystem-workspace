from typing import Any
from pydantic import BaseModel


class LabelStudioProject(BaseModel):
    id: int
    title: str
    task_number: int | None = None


class LabelStudioTask(BaseModel):
    id: int
    data: dict[str, Any]


class TaskCreateRequest(BaseModel):
    data: dict[str, Any]
