<p align="center">
  <img src="dev\github\logo\baby.png" alt="logo" width="160" style="border-radius:12px; box-shadow: 0 8px 24px rgba(33,37,41,0.12);"/>
</p>

# AI Ecosystem Workspace

A modular workspace for developing, experimenting, and integrating AI tools, models, and pipelines. This repository provides developer tooling, Python backend code, diagrams, utility scripts, and sandbox integrations for building AI-powered applications.

Use this repository as a local developer playground for model prototyping, data labeling workflows, and integration experiments.

## Table of Contents

- [Overview](#overview)
- [Current repository state](#current-repository-state)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Backend Architecture](#backend-architecture)
- [Environment & Dependencies](#environment--dependencies)
- [Services (Docker Compose)](#services-docker-compose)
- [API Documentation](#api-documentation)
- [Development Workflow](#development-workflow)
- [WTN-A08: MLflow and Inference Worker](#wtn-a08-mlflow-and-inference-worker)
- [ASM09: Observability Tools](#asm09-observability-tools)
- [What changed recently](#what-changed-recently)
- [Contributing](#contributing)
- [Contact](#contact)

## Overview

AI Ecosystem Workspace is designed as a lightweight, composable platform for AI experimentation and integration. It includes:

- **FastAPI Backend** - RESTful API with async job queue support
- **Async Workers** - Background task execution via arq
- **Data Annotation** - Label Studio integration for data labeling
- **Object Storage** - MinIO S3-compatible storage for datasets
- **Database** - PostgreSQL for persistent data
- **Caching & Queuing** - Redis for cache and async job queue
- **Docker Support** - Container images and Compose configuration for local and production deployments

## Current repository state

This update reflects the repository's current state as of the latest commit:

**Component Documentation Added:**
- ✅ Comprehensive README files for all major components
- ✅ API endpoint documentation (v1 routes: auth, health, training, arq, minio, labelstudio, postgres)
- ✅ Backend subpackage guides (api, core, libs, services, utils, workers)
- ✅ Sandbox integration examples (labelstudio, minio)
- ✅ Utility scripts documentation (export_openapi.py, enqueue_job.py, upload_dataset.py)
- ✅ Docker containerization guides

**Key locations:**
- Backend entry point: `backend/main.py`
- API routes: `backend/api/v1/` (auth, health, training, arq, minio, labelstudio, postgres)
- Database models: `backend/core/db/models.py`
- Async tasks: `backend/workers/tasks/` (simple_work.py, train_token_classifier.py)
- Services: `backend/services/` (auth, training, storage, annotation, job management)
- Utility scripts: `scripts/` (OpenAPI export, job enqueueing, dataset upload)
- Diagrams: `diagrams/overview.dio` and `diagrams/overview.png`

## Project Structure

[![GitHubTree](https://img.shields.io/badge/Structure-GitHubTree-blue?style=flat-square)](https://githubtree.mgks.dev/repo/jkznx/ai-ecosystem-workspace/main/)

```
ai-ecosystem-workspace/
├── README.md                           # This file
├── OVERVIEW.md                         # Older overview (reference)
├── compose.yml                         # Docker Compose configuration
├── pyproject.toml                      # Python dependencies
├── main.py                             # Example entry script
│
├── backend/                            # FastAPI backend application
│   ├── README.md                       # Backend overview
│   ├── main.py                         # Backend entry point
│   ├── api/                            # REST API routes & schemas
│   │   ├── README.md
│   │   ├── deps.py                     # Dependency injection
│   │   ├── schemas/                    # Pydantic request/response models
│   │   │   └── README.md
│   │   └── v1/                         # API v1 routes (organized by feature)
│   │       ├── README.md
│   │       ├── auth.py
│   │       ├── health.py
│   │       ├── arq/                    # Async queue endpoints
│   │       ├── training/               # Model training endpoints
│   │       ├── minio/                  # Object storage endpoints
│   │       ├── labelstudio/            # Data annotation endpoints
│   │       └── postgres/               # Database endpoints
│   ├── core/                           # Core utilities & configuration
│   │   ├── README.md
│   │   ├── config.py                   # Environment configuration
│   │   ├── logger.py                   # Logging setup
│   │   ├── security.py                 # Auth & encryption
│   │   ├── exceptions.py               # Custom exceptions
│   │   └── db/                         # Database layer
│   │       ├── README.md
│   │       ├── session.py              # SQLAlchemy session management
│   │       └── models.py               # ORM models
│   ├── libs/                           # External service clients
│   │   ├── README.md
│   │   ├── arq_pool.py                 # Async queue connection
│   │   ├── minio_client.py             # MinIO S3 client
│   │   ├── labelstudio_client.py       # Label Studio API client
│   │   └── redis_client.py             # Redis connection
│   ├── services/                       # Business logic layer
│   │   ├── README.md
│   │   ├── auth_service.py
│   │   ├── training_service.py
│   │   ├── job_service.py
│   │   ├── storage_service.py
│   │   ├── annotation_service.py
│   │   └── student_service.py
│   ├── utils/                          # Utility functions
│   │   └── README.md
│   └── workers/                        # Background job workers
│       ├── README.md
│       ├── worker_settings.py
│       └── tasks/                      # Async task definitions
│           ├── README.md
│           ├── simple_work.py
│           └── train_token_classifier.py
│
├── scripts/                            # Utility scripts for operations
│   ├── README.md
│   ├── export_openapi.py               # Export API documentation
│   ├── enqueue_job.py                  # Manually enqueue jobs
│   └── upload_dataset.py               # Upload datasets to MinIO
│
├── docs/                               # Project documentation
│   ├── README.md
│   └── api/                            # Generated API documentation
│       ├── README.md
│       ├── openapi.json                # OpenAPI 3.0 spec
│       ├── api-list.csv                # Endpoint list
│       └── api-list.xlsx
│
├── diagrams/                           # Architecture diagrams
│   ├── README.md
│   ├── overview.dio                    # Diagram source (draw.io)
│   └── overview.png                    # Rendered overview
│
├── sandbox/                            # Experimental integrations
│   ├── README.md
│   ├── test_settings.py
│   ├── labelstudio/                    # Label Studio examples
│   │   ├── README.md
│   │   ├── list_projects.py
│   │   └── list_tasks.py
│   └── minio/                          # MinIO examples
│       ├── README.md
│       ├── upload.py
│       ├── download.py
│       ├── list_versions.py
│       └── enable_versioning.py
│
├── docker/                             # Docker images
│   ├── README.md
│   ├── api.Dockerfile                  # API server image
│   └── trainer.Dockerfile              # Worker/trainer image
│
└── dev/                                # Development assets
    └── github/
        └── logo/
            └── baby.png
```

## Getting Started

### Prerequisites

- Git
- Docker & Docker Compose (for running services)
- Python 3.14+ (see `.python-version`)
- `uv` (optional) or pip for dependency management

### Quick Start (local development)

1. **Clone the repository**

```bash
git clone https://github.com/jkznx/ai-ecosystem-workspace.git
cd ai-ecosystem-workspace
```

2. **Create a Python virtual environment and install the project**

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
# or .\.venv\Scripts\activate on Windows (PowerShell)
pip install -e .
```

(If you use `uv`, run `uv sync` to apply the lockfile.)

3. **Start dependent services with Docker Compose (optional)**

```bash
docker compose -f compose.yml up -d
```

This starts:
- **FastAPI** backend (port 8000)
- **PostgreSQL** database (port 5432)
- **Redis** cache & queue (port 6379)
- **Label Studio** annotation UI (port 8080)
- **MinIO** S3 storage (port 9000)
- Background **worker** for async jobs

4. **Run the backend**

```bash
python backend/main.py
```

Or run with Uvicorn for interactive API docs:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Then visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/v1/health

## Backend Architecture

### API Structure (v1)

The backend organizes API endpoints into feature domains:

| Endpoint | Purpose | Notes |
|----------|---------|-------|
| `/v1/health` | Service health & readiness | DB, cache, external service checks |
| `/v1/auth` | User authentication | Login, token, refresh |
| `/v1/training` | Model training workflows | Start, monitor, download trained models |
| `/v1/arq` | Async job queue management | Enqueue, check status, list jobs |
| `/v1/minio` | Object storage operations | Upload/download datasets, manage buckets |
| `/v1/labelstudio` | Data annotation integration | Create projects, fetch annotations |
| `/v1/postgres` | Database health & schema | Table info, connection status |

See [docs/api/README.md](docs/api/README.md) and [backend/api/v1/README.md](backend/api/v1/README.md) for detailed API documentation.

### Backend Layers

1. **API Layer** (`backend/api/`) - HTTP route handlers, request/response validation
2. **Service Layer** (`backend/services/`) - Business logic, orchestration
3. **Data Layer** (`backend/core/db/`) - Database models, session management
4. **External Clients** (`backend/libs/`) - Third-party service integrations
5. **Workers** (`backend/workers/`) - Async task execution
6. **Core** (`backend/core/`) - Config, logging, security, exceptions

### Database Models

ORM models in `backend/core/db/models.py`:
- **User** - Application users
- **Student** - Student/learner records
- **Job** - Async job tracking
- (Extensible for your domain models)

### Async Jobs (arq)

Background job execution via arq queue:

- **Simple tasks** - `backend/workers/tasks/simple_work.py` (example)
- **ML training** - `backend/workers/tasks/train_token_classifier.py` (complex example)
- Job status tracked in Redis/database
- Monitored via `/v1/arq/` endpoints

## Environment & Dependencies

- `.python-version` - Target Python version (3.14)
- `pyproject.toml` - Python package metadata and dependencies
- `.env` - Environment variables (create from `.env.example` if provided)

### Key Dependencies

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM for database
- **Pydantic** - Data validation
- **arq** - Async job queue
- **minio** - S3-compatible storage
- **psycopg2** - PostgreSQL driver
- **redis** - Cache & queue backend

### Install dependencies

```bash
# Using pip
pip install -e .

# Using uv (faster)
uv sync
```

## Services (Docker Compose)

The `compose.yml` file configures all development services:

| Service | Port | Purpose |
|---------|------|---------|
| **api** | 8000 | FastAPI backend |
| **worker** | — | Background job worker |
| **postgres** | 5432 | Relational database |
| **redis** | 6379 | Cache & async queue |
| **label-studio** | 8080 | Data annotation UI |
| **minio** | 9000 | S3 object storage |

### Start services

```bash
docker compose -f compose.yml up -d
```

### Check service logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f api
docker compose logs -f worker
```

### Stop services

```bash
docker compose down
```

### Configure via .env

Create `.env` file to override defaults:

```env
# Backend
BACKEND_URL=http://localhost:8000

# Database
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_DB=ai_workspace

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_BUCKET=ai-datasets

# Label Studio
LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
```

## API Documentation

### Interactive API docs

When backend is running:

- **Swagger UI** (interactive): http://localhost:8000/docs
- **ReDoc** (read-only): http://localhost:8000/redoc
- **Raw OpenAPI JSON**: http://localhost:8000/openapi.json

### Export API documentation

Generate OpenAPI spec and endpoint lists:

```bash
python scripts/export_openapi.py
```

Creates:
- `docs/api/openapi.json` - Full OpenAPI 3.0 specification
- `docs/api/api-list.csv` - Endpoints in CSV format
- `docs/api/api-list.xlsx` - Endpoints in Excel format

See [scripts/README.md](scripts/README.md) for more details.

## Development Workflow

### Repository structure best practices

- **Backend code** → `backend/` - Production-quality code
  - Services, API routes, database models
  - Keep component READMEs updated
  - Write tests alongside code

- **Sandbox experiments** → `sandbox/` - Prototypes and experiments
  - Don't depend on sandbox artifacts
  - Use for quick testing and integration trials
  - Move proven code to `backend/`

- **Documentation** → `docs/` - Project docs and API specs
  - Generated API docs in `docs/api/`
  - Use `scripts/export_openapi.py` to update

- **Utilities** → `scripts/` - Operational scripts
  - Data loading, API export, job management
  - Add docstrings and configuration guide

- **Diagrams** → `diagrams/` - Architecture visuals
  - Source: `overview.dio` (draw.io format)
  - Export PNG when architecture changes

### Common development commands

```bash
# Start services
docker compose -f compose.yml up -d

# View logs
docker compose logs -f api

# Stop services
docker compose down

# Run backend (direct Python)
python backend/main.py

# Run backend with auto-reload
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Export API documentation
python scripts/export_openapi.py

# Enqueue a background job
python scripts/enqueue_job.py

# Upload dataset to MinIO
python scripts/upload_dataset.py
```

### Secrets management

- ⚠️ **Never commit secrets** (API keys, passwords, tokens)
- Use `.env` file for local development (add to `.gitignore`)
- Use environment variables or secrets manager for production
- See `compose.yml` for default development credentials

## What changed recently

### Latest commit
- ✅ **Comprehensive documentation added** for all components
  - 15 new/updated README files
  - API endpoint guides for v1 routes
  - Backend subpackage documentation
  - Sandbox integration examples
  - Utility scripts documentation
  - Docker containerization guide
  - Commit: [a32f874](https://github.com/jkznx/ai-ecosystem-workspace/commit/a32f87451d5d9c98f8e272f335b239a9ca3bfdfc)

### Previous commits
- Component README files added to document backend, diagrams, docs, scripts, and sandbox
  - Commit: [158251a](https://github.com/jkznx/ai-ecosystem-workspace/commit/158251a7b05f201b22e4326972b2e70db161d6b7)

### Next steps

- Consider adding `CHANGELOG.md` and semantic versioning
- Set up CI/CD pipeline (GitHub Actions)
- Add unit tests and integration tests
- Implement pre-commit hooks for code quality
- Set up automated API documentation updates

## Contributing

Contributions are welcome! Typical workflow:

1. **Fork and clone** the repository
2. **Create a feature branch** (`git checkout -b feature/my-feature`)
3. **Make changes** and keep component READMEs up-to-date
4. **Add tests** for new functionality
5. **Commit** with clear messages
6. **Open a pull request** describing the change

### Code guidelines

- Follow Python PEP 8 / PEP 484 (type hints)
- Add docstrings to functions and classes
- Write tests for business logic
- Keep dependencies minimal and documented
- Update relevant README files

### Security

- ⚠️ **Never commit secrets** or API keys
- Use `.env` files for local development
- Use environment variables or CI secrets for automation
- Review dependencies for vulnerabilities

## Contact

**Maintainer**: `jkznx`

**Questions or suggestions?**
- Open an issue: https://github.com/jkznx/ai-ecosystem-workspace/issues
- Check existing documentation in component README files
- Review commit history for implementation details

---

**Happy coding! 🚀**
