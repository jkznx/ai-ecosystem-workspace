from fastapi import APIRouter, Depends, status

from backend.api.deps import get_current_user, require_admin
from backend.api.schemas.training import (
    TrainingEnqueueResponse,
    TrainingRequest,
    TrainingStatusResponse,
)
from backend.core.db.models import User
from backend.services.training_service import training_service


router = APIRouter(
    prefix="/training",
    tags=["training"],
)


@router.post(
    "/enqueue",
    response_model=TrainingEnqueueResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def enqueue_training(
    body: TrainingRequest,
    _user: User = Depends(require_admin),
) -> TrainingEnqueueResponse:
    result = await training_service.enqueue(body)
    return TrainingEnqueueResponse(**result)


@router.get(
    "/status/{job_id}",
    response_model=TrainingStatusResponse,
)
async def get_training_status(
    job_id: str,
    _user: User = Depends(get_current_user),
) -> TrainingStatusResponse:
    result = await training_service.status(job_id)
    return TrainingStatusResponse(**result)


@router.get(
    "/jobs",
    response_model=list[TrainingStatusResponse],
)
async def list_training_jobs(
    _user: User = Depends(get_current_user),
) -> list[TrainingStatusResponse]:
    jobs = await training_service.list_jobs()

    return [
        TrainingStatusResponse(**job)
        for job in jobs
    ]