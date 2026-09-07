from __future__ import annotations

import logging
from time import perf_counter
from typing import Any

import mlflow
import mlflow.transformers
import torch
from mlflow import MlflowClient
from transformers import pipeline as build_pipeline

from backend.api.schemas.inference import InferenceRequest
from backend.core.config import settings

logger = logging.getLogger("inference-worker")
_PIPELINE_CACHE: dict[str, Any] = {}


def normalize_prediction(prediction: dict[str, Any]) -> dict:
    normalized = {}
    for key, value in prediction.items():
        if key == "score":
            normalized[key] = float(value)
        elif key in {"index", "start", "end"}:
            normalized[key] = None if value is None else int(value)
        else:
            normalized[key] = str(value)
    return normalized


def load_registered_pipeline(
    model_name: str,
    model_alias: str,
) -> tuple[Any, str, str]:
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    client = MlflowClient(tracking_uri=settings.MLFLOW_TRACKING_URI)
    model_version = client.get_model_version_by_alias(
        model_name,
        model_alias,
    )
    resolved_uri = f"models:/{model_name}/{model_version.version}"

    if resolved_uri not in _PIPELINE_CACHE:
        device = 0 if torch.cuda.is_available() else -1
        logger.info(
            "Loading MLflow model %s on device %s",
            resolved_uri,
            device,
        )
        _PIPELINE_CACHE.clear()
        components = mlflow.transformers.load_model(
            resolved_uri,
            return_type="components",
        )
        _PIPELINE_CACHE[resolved_uri] = build_pipeline(
            task="token-classification",
            model=components["model"],
            tokenizer=components["tokenizer"],
            device=device,
        )

    alias_uri = f"models:/{model_name}@{model_alias}"
    return (
        _PIPELINE_CACHE[resolved_uri],
        str(model_version.version),
        alias_uri,
    )


async def predict_token_classification(
    ctx: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    job_id = str(ctx["job_id"])
    request = InferenceRequest.model_validate(payload)
    started_at = perf_counter()

    inference_pipeline, model_version, model_uri = load_registered_pipeline(
        request.model_name,
        request.model_alias,
    )

    raw_predictions = inference_pipeline(
        request.text,
        aggregation_strategy=request.aggregation_strategy,
    )
    predictions = [normalize_prediction(prediction) for prediction in raw_predictions]
    duration_ms = (perf_counter() - started_at) * 1000
    model_device = next(inference_pipeline.model.parameters()).device
    if model_device.type == "cuda":
        device_index = model_device.index or 0
        device = f"{torch.cuda.get_device_name(device_index)} " f"({model_device})"
    else:
        device = str(model_device)

    logger.info(
        "Inference job %s completed with %d entities",
        job_id,
        len(predictions),
    )
    return {
        "job_id": job_id,
        "model_uri": model_uri,
        "model_version": model_version,
        "text": request.text,
        "predictions": predictions,
        "duration_ms": round(duration_ms, 2),
        "device": device,
    }
