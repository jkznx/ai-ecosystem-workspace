from fastapi import APIRouter, Depends, status

from backend.api.deps import get_current_user
from backend.api.schemas.inference import (
    InferenceEnqueueResponse,
    InferenceRequest,
    InferenceStatusResponse,
)
from backend.core.db.models import User
from backend.services.inference_service import inference_service

router = APIRouter(
    prefix="/inference",
    tags=["inference"],
)


@router.post(
    "/predict",
    response_model=InferenceStatusResponse,
)
async def predict(
    body: InferenceRequest,
    _user: User = Depends(get_current_user),
) -> InferenceStatusResponse:
    result = await inference_service.predict_and_wait(body)
    return InferenceStatusResponse(**result)


@router.post(
    "/enqueue",
    response_model=InferenceEnqueueResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def enqueue_inference(
    body: InferenceRequest,
    _user: User = Depends(get_current_user),
) -> InferenceEnqueueResponse:
    result = await inference_service.enqueue(body)
    return InferenceEnqueueResponse(**result)


@router.get(
    "/status/{job_id}",
    response_model=InferenceStatusResponse,
)
async def get_inference_status(
    job_id: str,
    _user: User = Depends(get_current_user),
) -> InferenceStatusResponse:
    result = await inference_service.status(job_id)
    return InferenceStatusResponse(**result)


@router.get(
    "/jobs",
    response_model=list[InferenceStatusResponse],
)
async def list_inference_jobs(
    _user: User = Depends(get_current_user),
) -> list[InferenceStatusResponse]:
    jobs = await inference_service.list_jobs()
    return [InferenceStatusResponse(**job) for job in jobs]
