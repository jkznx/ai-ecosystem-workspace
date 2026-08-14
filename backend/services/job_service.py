from arq.jobs import Job

from backend.core.exceptions import ConflictError
from backend.libs.arq_pool import get_arq_pool

_JOB_REGISTRY_KEY = "api:job_ids"


class JobService:
    async def enqueue(self, function: str, args: list, kwargs: dict) -> str:
        pool = await get_arq_pool()
        job = await pool.enqueue_job(function, *args, **kwargs)
        if job is None:
            raise ConflictError("job could not be enqueued")
        await pool.sadd(_JOB_REGISTRY_KEY, job.job_id)
        return job.job_id

    async def status(self, job_id: str) -> dict:
        pool = await get_arq_pool()
        job = Job(job_id, pool)
        status_name = await job.status()
        result = None
        if status_name.name == "complete":
            info = await job.result_info()
            result = info.result if info else None
        return {"job_id": job_id, "status": status_name.name, "result": result}

    async def cancel(self, job_id: str) -> bool:
        pool = await get_arq_pool()
        return await Job(job_id, pool).abort()

    async def list_all(self) -> list[dict]:
        pool = await get_arq_pool()
        job_ids = await pool.smembers(_JOB_REGISTRY_KEY)
        out = []
        for jid in job_ids:
            jid_str = jid.decode() if isinstance(jid, bytes) else jid
            st = await Job(jid_str, pool).status()
            out.append({"job_id": jid_str, "status": st.name})
        return out


job_service = JobService()