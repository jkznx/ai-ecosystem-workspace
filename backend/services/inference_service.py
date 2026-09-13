from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from uuid import uuid4

from arq.jobs import Job, JobStatus

from backend.api.schemas.inference import InferenceRequest
from backend.core.config import settings
from backend.core.exceptions import ConflictError, NotFoundError
from backend.libs.arq_pool import get_arq_pool
from backend.observability.telemetry import inject_trace_context

INFERENCE_JOB_REGISTRY_KEY = "inference:job_ids"
INFERENCE_JOB_METADATA_PREFIX = "inference:job:metadata:"


def metadata_key(job_id: str) -> str:
    return f"{INFERENCE_JOB_METADATA_PREFIX}{job_id}"


def json_value(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool, list, dict)):
        return value
    return str(value)


class InferenceService:
    async def enqueue(
        self,
        request: InferenceRequest,
    ) -> dict:
        pool = await get_arq_pool()
        submitted_at = datetime.now(timezone.utc)
        job_id = f"infer-{submitted_at.strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"

        job = await pool.enqueue_job(
            "predict_token_classification",
            request.model_dump(mode="json"),
            inject_trace_context(),
            _job_id=job_id,
            _queue_name=settings.INFERENCE_QUEUE_NAME,
            _expires=(
                settings.INFERENCE_JOB_TIMEOUT_SECONDS
                + settings.INFERENCE_RESULT_TTL_SECONDS
            ),
        )

        if job is None:
            raise ConflictError("Inference job could not be enqueued")

        metadata = {
            "job_id": job_id,
            "queue_name": settings.INFERENCE_QUEUE_NAME,
            "submitted_at": submitted_at.isoformat(),
            "model_uri": request.model_uri,
        }

        await pool.sadd(INFERENCE_JOB_REGISTRY_KEY, job_id)
        await pool.set(
            metadata_key(job_id),
            json.dumps(metadata),
            ex=settings.INFERENCE_RESULT_TTL_SECONDS,
        )

        return {
            **metadata,
            "status": "queued",
        }

    async def status(self, job_id: str) -> dict:
        pool = await get_arq_pool()
        job = Job(
            job_id,
            pool,
            _queue_name=settings.INFERENCE_QUEUE_NAME,
        )
        job_status = await job.status()

        if job_status == JobStatus.not_found:
            raise NotFoundError(f"Inference job {job_id!r} was not found")

        metadata = {}
        metadata_raw = await pool.get(metadata_key(job_id))
        if metadata_raw:
            if isinstance(metadata_raw, bytes):
                metadata_raw = metadata_raw.decode("utf-8")
            metadata = json.loads(metadata_raw)

        success = None
        result = None
        if job_status == JobStatus.complete:
            result_info = await job.result_info()
            if result_info is not None:
                success = result_info.success
                result = json_value(result_info.result)

        return {
            "job_id": job_id,
            "queue_name": settings.INFERENCE_QUEUE_NAME,
            "status": job_status.value,
            "submitted_at": metadata.get("submitted_at"),
            "model_uri": metadata.get("model_uri"),
            "success": success,
            "result": result,
        }

    async def predict_and_wait(
        self,
        request: InferenceRequest,
    ) -> dict:
        enqueued = await self.enqueue(request)
        job_id = enqueued["job_id"]
        loop = asyncio.get_running_loop()
        deadline = loop.time() + settings.INFERENCE_API_WAIT_SECONDS

        while True:
            current = await self.status(job_id)
            if current["status"] == JobStatus.complete.value:
                return current
            if loop.time() >= deadline:
                return current
            await asyncio.sleep(0.25)

    async def list_jobs(self) -> list[dict]:
        pool = await get_arq_pool()
        raw_job_ids = await pool.smembers(INFERENCE_JOB_REGISTRY_KEY)
        jobs = []

        for raw_job_id in raw_job_ids:
            job_id = (
                raw_job_id.decode("utf-8")
                if isinstance(raw_job_id, bytes)
                else str(raw_job_id)
            )
            try:
                jobs.append(await self.status(job_id))
            except NotFoundError:
                await pool.srem(
                    INFERENCE_JOB_REGISTRY_KEY,
                    job_id,
                )

        jobs.sort(
            key=lambda item: item.get("submitted_at") or "",
            reverse=True,
        )
        return jobs


inference_service = InferenceService()
