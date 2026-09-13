from __future__ import annotations

import json
from datetime import timezone
from uuid import uuid4

from arq.jobs import Job, JobStatus
from minio.error import S3Error

from backend.api.schemas.training import TrainingRequest
from backend.core.config import settings
from backend.core.exceptions import ConflictError, NotFoundError
from backend.libs.arq_pool import get_arq_pool
from backend.libs.minio_client import get_minio_client
from backend.observability.telemetry import inject_trace_context

TRAINING_JOB_REGISTRY_KEY = "trainer:job_ids"
TRAINING_JOB_METADATA_PREFIX = "trainer:job:metadata:"


def metadata_key(job_id: str) -> str:
    return f"{TRAINING_JOB_METADATA_PREFIX}{job_id}"


def convert_result_to_json_value(value: object) -> object:
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool, list, dict)):
        return value

    return str(value)


class TrainingService:
    def validate_dataset_exists(
        self,
        request: TrainingRequest,
    ) -> None:
        client = get_minio_client()

        try:
            client.stat_object(
                bucket_name=request.dataset_bucket,
                object_name=request.dataset_object,
            )
        except S3Error as error:
            if error.code in {
                "NoSuchBucket",
                "NoSuchKey",
                "NoSuchObject",
            }:
                raise NotFoundError(
                    "Training dataset was not found in MinIO"
                ) from error

            raise

    async def enqueue(
        self,
        request: TrainingRequest,
    ) -> dict:
        self.validate_dataset_exists(request)

        pool = await get_arq_pool()

        scheduled_for = request.start_at.astimezone(timezone.utc)
        timestamp = scheduled_for.strftime("%Y%m%dT%H%M%SZ")

        job_id = f"train-{request.model_name}-{timestamp}-{uuid4().hex[:8]}"

        payload = request.model_dump(mode="json")

        job = await pool.enqueue_job(
            "train_token_classifier",
            payload,
            inject_trace_context(),
            _job_id=job_id,
            _queue_name=settings.TRAINER_QUEUE_NAME,
            _defer_until=scheduled_for,
            _expires=settings.TRAINER_JOB_TIMEOUT_SECONDS + 86400,
        )

        if job is None:
            raise ConflictError("Training job could not be enqueued")

        metadata = {
            "job_id": job_id,
            "queue_name": settings.TRAINER_QUEUE_NAME,
            "scheduled_for": scheduled_for.isoformat(),
            "model_name": request.model_name,
            "dataset_bucket": request.dataset_bucket,
            "dataset_object": request.dataset_object,
        }

        await pool.sadd(
            TRAINING_JOB_REGISTRY_KEY,
            job_id,
        )

        await pool.set(
            metadata_key(job_id),
            json.dumps(metadata),
            ex=settings.TRAINER_RESULT_TTL_SECONDS,
        )

        return {
            "job_id": job_id,
            "queue_name": settings.TRAINER_QUEUE_NAME,
            "status": "deferred",
            "scheduled_for": scheduled_for,
        }

    async def status(
        self,
        job_id: str,
    ) -> dict:
        pool = await get_arq_pool()

        job = Job(
            job_id,
            pool,
            _queue_name=settings.TRAINER_QUEUE_NAME,
        )

        job_status = await job.status()

        if job_status == JobStatus.not_found:
            raise NotFoundError(f"Training job {job_id!r} was not found")

        metadata_raw = await pool.get(metadata_key(job_id))
        scheduled_for = None

        if metadata_raw:
            if isinstance(metadata_raw, bytes):
                metadata_raw = metadata_raw.decode("utf-8")

            metadata = json.loads(metadata_raw)
            scheduled_for = metadata.get("scheduled_for")

        success = None
        result = None

        if job_status == JobStatus.complete:
            result_info = await job.result_info()

            if result_info is not None:
                success = result_info.success
                result = convert_result_to_json_value(result_info.result)

        return {
            "job_id": job_id,
            "queue_name": settings.TRAINER_QUEUE_NAME,
            "status": job_status.value,
            "scheduled_for": scheduled_for,
            "success": success,
            "result": result,
        }

    async def list_jobs(self) -> list[dict]:
        pool = await get_arq_pool()
        raw_job_ids = await pool.smembers(TRAINING_JOB_REGISTRY_KEY)

        jobs = []

        for raw_job_id in raw_job_ids:
            if isinstance(raw_job_id, bytes):
                job_id = raw_job_id.decode("utf-8")
            else:
                job_id = str(raw_job_id)

            try:
                jobs.append(await self.status(job_id))
            except NotFoundError:
                await pool.srem(
                    TRAINING_JOB_REGISTRY_KEY,
                    job_id,
                )

        jobs.sort(
            key=lambda item: item.get("scheduled_for") or "",
            reverse=True,
        )

        return jobs


training_service = TrainingService()
