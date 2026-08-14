# backend/workers

Purpose:
- Background workers, tasks, and job processors (e.g., Celery, RQ, or custom workers).

Current state:
- Directory present; worker implementations likely called from `scripts/enqueue_job.py` or from the service layer.

How to use:
- Use `scripts/enqueue_job.py` to enqueue work against available workers.

Notes / next steps:
- Document the worker queue backend, required broker configuration, and how to run worker processes.
