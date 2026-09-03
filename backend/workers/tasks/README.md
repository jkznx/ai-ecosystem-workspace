# Worker Tasks

Asynchronous job tasks executed by the background worker (arq-based queue).

## Current tasks

- **simple_work.py** - Basic example task demonstrating job queueing
- **train_token_classifier.py** - Complex ML training task for token classification models

## How tasks work

1. Tasks are Python functions decorated with `@job` or registered in the arq task registry
2. Enqueued via job service or REST API (e.g., `POST /v1/arq/enqueue`)
3. Executed asynchronously by the worker process
4. Status and results stored in Redis or database

## Example task

```python
# tasks/my_task.py
async def my_task(param1, param2):
    """Async task that runs in the background."""
    result = do_work(param1, param2)
    return result
```

## Enqueueing a task

```python
from backend.libs.arq_pool import get_arq_pool

pool = await get_arq_pool()
job = await pool.enqueue_job('my_task', param1='value1', param2='value2')
print(f"Job ID: {job.job_id}")
```

## Monitoring tasks

- Use `/v1/arq/status/{job_id}` endpoint to check job status
- View worker logs: `docker compose logs worker` or check logs files
- Redis console for queue inspection

## Best practices

- Keep tasks idempotent (safe to retry)
- Log progress and errors within tasks
- Handle timeouts gracefully
- Test tasks locally before deployment
