from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import get_current_user
from backend.api.schemas.arq import JobEnqueueRequest, JobEnqueueResponse, JobStatusResponse
from backend.core.db.models import User
from backend.services.job_service import job_service

router = APIRouter(prefix="/arq", tags=["arq"])


@router.post("/store/enqueue", response_model=JobEnqueueResponse)
async def enqueue(body: JobEnqueueRequest, user: User = Depends(get_current_user)) -> JobEnqueueResponse:
    job_id = await job_service.enqueue(body.function, body.args, body.kwargs)
    return JobEnqueueResponse(job_id=job_id)


@router.delete("/store/cancel/{job_id}", status_code=204)
async def cancel(job_id: str, user: User = Depends(get_current_user)) -> None:
    if not await job_service.cancel(job_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Job cannot be cancelled")


@router.get("/load/status/{job_id}", response_model=JobStatusResponse)
async def load_status(job_id: str, user: User = Depends(get_current_user)) -> JobStatusResponse:
    return JobStatusResponse(**await job_service.status(job_id))


@router.get("/load/list", response_model=list[JobStatusResponse])
async def load_list(user: User = Depends(get_current_user)) -> list[JobStatusResponse]:
    return [JobStatusResponse(**j) for j in await job_service.list_all()]
