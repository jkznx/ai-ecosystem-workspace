# API Schemas

Pydantic models for request and response validation across all API endpoints.

## Current schemas

- **auth.py** - Authentication request/response models (LoginRequest, TokenResponse, etc.)
- **training.py** - Training job models (TrainingRequest, TrainingStatus, etc.)
- **arq.py** - Async queue job models (JobStatus, JobResult, etc.)
- **labelstudio.py** - Label Studio integration models
- **minio.py** - MinIO object storage models
- **postgres.py** - PostgreSQL database status models
- **__init__.py** - Exports all schema classes for convenience

## How to use

- Import schemas from this package: `from backend.api.schemas import LoginRequest, TokenResponse`
- Use in FastAPI route handlers for request/response validation
- Extend with new schemas as needed for new endpoints
- Keep schema versions in sync with API version (currently v1)

## Best practices

- Use descriptive field names with type hints
- Add docstrings and field descriptions for API documentation
- Keep models focused and composable (avoid overly large schemas)
- Use pydantic validators for custom validation logic
