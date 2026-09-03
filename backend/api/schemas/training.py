import re
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, ValidationInfo, field_validator


MODEL_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}$")


class TrainingRequest(BaseModel):
    dataset_name: str = "conll2003"
    dataset_bucket: str = "training-datasets"
    dataset_object: str = (
        "datasets/conll2003/v1/conll2003.tar.gz"
    )

    base_model: str = "bert-base-cased"
    model_name: str

    start_at: datetime

    epochs: int = Field(default=3, ge=1, le=20)
    batch_size: int = Field(default=4, ge=1, le=16)
    learning_rate: float = Field(default=2e-5, gt=0)

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, value: str) -> str:
        value = value.strip()

        if not MODEL_NAME_PATTERN.fullmatch(value):
            raise ValueError(
                "model_name may contain only letters, numbers, "
                "dot, underscore and hyphen"
            )

        return value

    @field_validator("dataset_bucket")
    @classmethod
    def validate_bucket_name(cls, value: str) -> str:
        value = value.strip()

        if not value or "/" in value or "\\" in value or ".." in value:
            raise ValueError("invalid dataset bucket")

        return value

    @field_validator("dataset_object")
    @classmethod
    def validate_dataset_object(cls, value: str) -> str:
        value = value.strip().lstrip("/")

        if not value or ".." in value or "\\" in value:
            raise ValueError("invalid dataset object key")

        return value

    @field_validator("start_at")
    @classmethod
    def validate_start_time(
        cls,
        value: datetime,
        info: ValidationInfo,
    ) -> datetime:
        if value.tzinfo is None:
            raise ValueError("start_at must include timezone information")

        value = value.astimezone(timezone.utc)

        allow_past_start_at = bool(
            info.context
            and info.context.get("allow_past_start_at")
        )

        if (
            not allow_past_start_at
            and value <= datetime.now(timezone.utc)
        ):
            raise ValueError("start_at must be in the future")

        return value


class TrainingEnqueueResponse(BaseModel):
    job_id: str
    queue_name: str
    status: str
    scheduled_for: datetime


class TrainingStatusResponse(BaseModel):
    job_id: str
    queue_name: str
    status: str
    scheduled_for: datetime | None = None
    success: bool | None = None
    result: Any | None = None
