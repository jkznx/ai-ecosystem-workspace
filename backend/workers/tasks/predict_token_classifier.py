from __future__ import annotations

from time import perf_counter
from typing import Any

import mlflow
import mlflow.transformers
import torch
from mlflow import MlflowClient
from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode
from transformers import pipeline as build_pipeline

from backend.api.schemas.inference import InferenceRequest
from backend.core.config import settings
from backend.core.logger import get_logger
from backend.observability.metrics import observe_inference_job
from backend.observability.telemetry import extract_trace_context

logger = get_logger("inference-worker")
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
) -> tuple[Any, str, str, bool]:
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    client = MlflowClient(tracking_uri=settings.MLFLOW_TRACKING_URI)
    model_version = client.get_model_version_by_alias(
        model_name,
        model_alias,
    )
    resolved_uri = f"models:/{model_name}/{model_version.version}"

    cache_hit = resolved_uri in _PIPELINE_CACHE
    if not cache_hit:
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
        cache_hit,
    )


async def predict_token_classification(
    ctx: dict[str, Any],
    payload: dict[str, Any],
    trace_context: dict[str, str] | None = None,
) -> dict[str, Any]:
    job_id = str(ctx["job_id"])
    request = InferenceRequest.model_validate(payload)
    started_at = perf_counter()
    entity_count = 0
    status = "failed"
    parent_context = extract_trace_context(trace_context)
    tracer = trace.get_tracer("ai-ecosystem.inference")

    with tracer.start_as_current_span(
        "inference.process",
        context=parent_context,
        kind=SpanKind.CONSUMER,
        attributes={
            "messaging.destination.name": settings.INFERENCE_QUEUE_NAME,
            "messaging.operation.type": "process",
            "job.id": job_id,
            "ai.model.name": request.model_name,
            "ai.model.alias": request.model_alias,
            "ai.input.characters": len(request.text),
        },
    ) as span:
        try:
            with tracer.start_as_current_span("mlflow.load_registered_model"):
                (
                    inference_pipeline,
                    model_version,
                    model_uri,
                    cache_hit,
                ) = load_registered_pipeline(
                    request.model_name,
                    request.model_alias,
                )

            with tracer.start_as_current_span("transformers.token_classification"):
                raw_predictions = inference_pipeline(
                    request.text,
                    aggregation_strategy=request.aggregation_strategy,
                )
            predictions = [
                normalize_prediction(prediction) for prediction in raw_predictions
            ]
            entity_count = len(predictions)
            duration_ms = (perf_counter() - started_at) * 1000
            model_device = next(inference_pipeline.model.parameters()).device
            if model_device.type == "cuda":
                device_index = model_device.index or 0
                device = f"{torch.cuda.get_device_name(device_index)} ({model_device})"
            else:
                device = str(model_device)

            span.set_attributes(
                {
                    "ai.model.version": model_version,
                    "ai.model.cache_hit": cache_hit,
                    "ai.output.entities": entity_count,
                    "ai.device": device,
                    "job.duration_ms": duration_ms,
                }
            )
            status = "success"
            logger.info(
                "Inference job %s completed with %d entities (cache_hit=%s)",
                job_id,
                entity_count,
                cache_hit,
            )
            return {
                "job_id": job_id,
                "model_uri": model_uri,
                "model_version": model_version,
                "text": request.text,
                "predictions": predictions,
                "duration_ms": round(duration_ms, 2),
                "device": device,
                "cache_hit": cache_hit,
            }
        except Exception as error:
            span.record_exception(error)
            span.set_status(Status(StatusCode.ERROR, str(error)))
            logger.exception("Inference job %s failed", job_id)
            raise
        finally:
            observe_inference_job(
                status=status,
                model_name=request.model_name,
                duration_seconds=perf_counter() - started_at,
                entity_count=entity_count,
            )
