import re
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

MODEL_REFERENCE_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}$")


class InferenceRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    model_name: str = "bert-conll2003-v1"
    model_alias: str = "champion"
    aggregation_strategy: Literal[
        "none",
        "simple",
        "first",
        "average",
        "max",
    ] = "simple"

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text must not be blank")
        return value

    @field_validator("model_name", "model_alias")
    @classmethod
    def validate_model_reference(cls, value: str) -> str:
        value = value.strip()
        if not MODEL_REFERENCE_PATTERN.fullmatch(value):
            raise ValueError(
                "model references may contain only letters, numbers, "
                "dot, underscore and hyphen"
            )
        return value

    @property
    def model_uri(self) -> str:
        return f"models:/{self.model_name}@{self.model_alias}"


class InferenceEnqueueResponse(BaseModel):
    job_id: str
    queue_name: str
    status: str
    model_uri: str


class InferenceStatusResponse(BaseModel):
    job_id: str
    queue_name: str
    status: str
    submitted_at: str | None = None
    model_uri: str | None = None
    success: bool | None = None
    result: Any | None = None
