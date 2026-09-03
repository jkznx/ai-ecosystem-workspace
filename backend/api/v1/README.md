# API v1

FastAPI route handlers for API version 1, organized by feature domain.

## Route groups

- **auth.py** - Authentication (login, logout, token refresh)
- **health.py** - Service health checks (database, cache, external services)
- **arq/** - Async job queue operations (list jobs, get status, enqueue)
- **training/** - Model training (start training, get status, download model)
- **minio/** - Object storage (upload, download, list buckets)
- **labelstudio/** - Data annotation (create tasks, fetch annotations)
- **postgres/** - Database operations (migrations, schema info)

## How to use

- Each route group is a Python module or package under `v1/`
- Routes are registered in `backend/main.py` via `router = APIRouter()` and `app.include_router()`
- Request/response schemas are defined in `backend/api/schemas/`
- Use dependency injection from `backend/api/deps.py` (e.g., `Depends(get_current_user)`)

## Adding new endpoints

1. Create a new file or directory under `v1/` (e.g., `v1/my_feature.py`)
2. Define route handlers using FastAPI decorators (`@router.get()`, `@router.post()`, etc.)
3. Import or define request/response schemas
4. Import and register the router in `backend/main.py`
5. Test with `curl`, Postman, or the interactive docs at `/docs`
