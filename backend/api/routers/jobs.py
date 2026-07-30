from fastapi import APIRouter, Depends, HTTPException, status
from arq import create_pool
from arq.connections import RedisSettings
from arq.jobs import Job

from backend.api.deps import get_current_user
from backend.api.schemas import JobEnqueueRequest, JobEnqueueResponse, JobStatusResponse
from backend.core.config import settings
from backend.core.db.models import User

router = APIRouter(prefix="/jobs", tags=["jobs"])
_JOB_REGISTRY_KEY = "api:job_ids"


async def _get_pool():
    return await create_pool(
        RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT, database=settings.REDIS_DB)
    )


@router.post("/enqueue", response_model=JobEnqueueResponse)
async def enqueue(body: JobEnqueueRequest, user: User = Depends(get_current_user)) -> JobEnqueueResponse:
    pool = await _get_pool()
    job = await pool.enqueue_job(body.function, *body.args, **body.kwargs)
    if job is None:
        raise HTTPException(status_code=400, detail="Job could not be enqueued")
    await pool.sadd(_JOB_REGISTRY_KEY, job.job_id)
    return JobEnqueueResponse(job_id=job.job_id)


@router.get("/{job_id}", response_model=JobStatusResponse)
async def job_status(job_id: str, user: User = Depends(get_current_user)) -> JobStatusResponse:
    pool = await _get_pool()
    job = Job(job_id, pool)
    status_name = await job.status()
    result = None
    if status_name.name == "complete":
        info = await job.result_info()
        result = info.result if info else None
    return JobStatusResponse(job_id=job_id, status=status_name.name, result=result)


@router.delete("/{job_id}", status_code=204)
async def cancel_job(job_id: str, user: User = Depends(get_current_user)) -> None:
    pool = await _get_pool()
    job = Job(job_id, pool)
    aborted = await job.abort()
    if not aborted:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Job cannot be cancelled")


@router.get("/")
async def list_jobs(user: User = Depends(get_current_user)) -> list[JobStatusResponse]:
    pool = await _get_pool()
    job_ids = await pool.smembers(_JOB_REGISTRY_KEY)
    results = []
    for jid in job_ids:
        jid_str = jid.decode() if isinstance(jid, bytes) else jid
        st = await Job(jid_str, pool).status()
        results.append(JobStatusResponse(job_id=jid_str, status=st.name))
    return results