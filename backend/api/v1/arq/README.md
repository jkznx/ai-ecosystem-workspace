# ARQ (Async Queue) API

Endpoints for managing background jobs via the arq async queue.

## Endpoints

- `GET /v1/arq/status/{job_id}` - Get job status and result
- `GET /v1/arq/jobs` - List recent jobs
- `POST /v1/arq/enqueue` - Enqueue a new job
- `DELETE /v1/arq/jobs/{job_id}` - Cancel/delete a job

## Job lifecycle

1. **Enqueued** - Job added to queue, waiting for worker
2. **Running** - Worker picked up and executing job
3. **Complete** - Job finished successfully
4. **Failed** - Job failed with error

## How to use

```bash
# Enqueue a job
curl -X POST http://localhost:8000/v1/arq/enqueue \
  -H "Content-Type: application/json" \
  -d '{"task": "train_token_classifier", "args": {"dataset_id": "123"}}'

# Check status
curl http://localhost:8000/v1/arq/status/{job_id}
```
