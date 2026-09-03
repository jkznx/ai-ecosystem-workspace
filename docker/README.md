# Docker

Dockerfiles for building container images for the AI Ecosystem Workspace.

## Images

- **api.Dockerfile** - FastAPI backend API server
- **trainer.Dockerfile** - Background worker for async training jobs

## Building images

```bash
# Build API image
docker build -f docker/api.Dockerfile -t ai-ecosystem:api .

# Build trainer/worker image
docker build -f docker/trainer.Dockerfile -t ai-ecosystem:trainer .
```

## Running containers

```bash
# Run API
docker run -p 8000:8000 ai-ecosystem:api

# Run trainer worker
docker run ai-ecosystem:trainer
```

## Docker Compose

For local development, use `compose.yml` to run all services:

```bash
docker compose -f compose.yml up
```

This starts:
- FastAPI backend (port 8000)
- Background worker
- PostgreSQL database
- Redis cache
- Label Studio annotation UI
- MinIO object storage

## Production deployment

For production:
1. Use a container registry (Docker Hub, ECR, etc.)
2. Tag images with versions: `ai-ecosystem:api-v1.0.0`
3. Use container orchestration (Kubernetes, Docker Swarm, etc.)
4. Configure environment variables securely
5. Use health checks and logging

## Customization

Edit Dockerfiles to:
- Change base images (Python version, etc.)
- Add additional dependencies
- Set working directory and entry points
- Configure environment variables
