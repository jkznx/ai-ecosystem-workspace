# Backend API

Contains the API layer for the backend, including HTTP route handlers, endpoint definitions, request/response schemas, and dependency injection.

## Structure

- **deps.py** - Dependency injection functions (e.g., getting current user, database session)
- **schemas/** - Pydantic models for request/response validation
- **v1/** - API v1 route handlers organized by feature/domain

## API Versions

- **v1** - Current API version with endpoints for health checks, authentication, training, storage, and more

## How to use

- Add new route handlers in `v1/` subdirectories
- Define request/response schemas in `schemas/`
- Use dependency injection from `deps.py` in route handlers (e.g., `get_current_user`, `get_db`)
- Endpoints are registered in the main app in `backend/main.py`

## Key endpoints

- `/v1/health` - Health check endpoints
- `/v1/auth` - Authentication endpoints
- `/v1/training` - Model training endpoints
- `/v1/arq` - Async job queue endpoints
- `/v1/minio` - Object storage endpoints
- `/v1/labelstudio` - Data annotation service endpoints
- `/v1/postgres` - Database status endpoints
