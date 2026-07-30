# AI Ecosystem Workspace

A modular workspace for developing, experimenting, and integrating AI tools, models, and pipelines. This repository provides a containerized environment with essential services and developer tooling for building and testing small-to-medium AI projects locally.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment](#environment)
- [Services](#services)
- [FastAPI Example](#fastapi-example)
- [Dependencies](#dependencies)
- [Development Workflow](#development-workflow)
- [Contributing](#contributing)
- [Contact](#contact)

## Overview

AI Ecosystem Workspace is designed as a lightweight, composable platform for AI experimentation and integration. It uses Docker Compose to orchestrate services and includes Python tooling for data processing, model experimentation, and simple backend services.

Key use cases:
- Rapid prototyping of AI models and data pipelines
- Data labeling and annotation workflows using Label Studio
- Local S3-compatible object storage using MinIO
- Simple relational database backed by PostgreSQL
- Background/async job processing with Redis and arq

## Key Features

- Multi-service Docker Compose setup
- Label Studio for annotation workflows
- MinIO for S3-compatible object storage
- PostgreSQL for structured data
- Redis for caching and async queues
- Python tooling with modern dependency management (uv)
- Minimal FastAPI example app with Uvicorn for local development and testing

## Project Structure

```
ai-ecosystem-workspace/
├── README.md              # This file
├── compose.yml            # Docker Compose services configuration
├── pyproject.toml         # Python project metadata and dependencies
├── main.py                # Main entry point (example)
├── .python-version        # Python version specification
├── uv.lock                # Locked dependencies for uv
├── backend/               # Backend application code (placeholder)
│   └── app/
│       └── main.py        # Example FastAPI app (recommended location)
├── sandbox/               # Experimentation and prototyping area
├── diagrams/              # Architecture and documentation diagrams
└── out.jpg                # Generated output/visualization
```

Note: `compose.yml` is the repository's Docker Compose configuration. The backend and sandbox folders are intended as starting points; add modules and experiments as needed.

## Getting Started

### Prerequisites

- Git (latest stable)
- Docker & Docker Compose (for running services)
- Python 3.14+ (for local development; see `.python-version`)
- uv (recommended) or pip for dependency management

### Quick Start

1. Clone the repository

```bash
git clone https://github.com/jkznx/ai-ecosystem-workspace.git
cd ai-ecosystem-workspace
```

2. Configure environment variables

Create a `.env` file in the repository root (example values shown):

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=label_studio
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379

# MinIO
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=aegis@810vii
MINIO_CONSOLE_PORT=9001
MINIO_API_PORT=9000

# Label Studio
LABEL_STUDIO_PORT=8080
```

Avoid committing secrets to the repo. For production or shared environments, override credentials using a secure secrets manager.

3. Install Python dependencies

Using uv (recommended):

```bash
uv sync
```

Or using venv + pip:

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.\.venv\Scripts\activate   # Windows (PowerShell)
pip install -e .
```

If you plan to run the example FastAPI app locally install FastAPI and Uvicorn (if not already included in your project dependencies):

```bash
pip install fastapi uvicorn[standard]
```

4. Start Docker services

```bash
docker compose -f compose.yml up -d
```

This will start services described below (Redis, PostgreSQL, Label Studio, MinIO).

5. Run the application example

- To run the simple example `main.py`:

```bash
python main.py
```

- To run the FastAPI example (if you add or use the example backend/app/main.py):

```bash
# from repository root
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for the automatic interactive API docs when running with `--reload`.

## Environment

- Python: .python-version contains the target Python version (3.14+ by default in this repo).
- Dependency lock: `uv.lock` is used when working with the `uv` package manager.

## Services

The Compose configuration brings up several services. The descriptions below reflect the current setup in this repository.

### Redis
- Image: `redis:8.8.0-alpine`
- Port: 6379 (container port)
- Purpose: Caching and async job queues (used with `arq`)
- Persistence: AOF or volume-backed persistence is recommended for non-transient state

### PostgreSQL
- Image: `postgres:16-alpine`
- Port: 5432 (container port) mapped to host 5433 in the example compose
- Default credentials (development):
  - User: `postgres`
  - Password: `postgres`
  - Database: `label_studio`

> Tip: Use the `.env` file to override these values before starting services.

### Label Studio
- Image: `heartexlabs/label-studio:latest`
- Port: 8080
- Purpose: Data labeling and annotation interface
- Database: Configurable to use the PostgreSQL service in this compose setup

### MinIO
- Image: `minio/minio:latest`
- Ports:
  - 9000 (S3 API)
  - 9001 (Web console)
- Purpose: Object storage (S3-compatible)
- Default development credentials (see `.env`):
  - Access Key: `minioadmin`
  - Secret Key: `aegis@810vii`

## FastAPI Example

A minimal FastAPI app is a recommended addition for serving small APIs or demoing model inference locally. Place an example app at `backend/app/main.py` with contents similar to:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/hello")
async def hello(name: str = "world"):
    return {"message": f"hello, {name}"}
```

Run it with Uvicorn as shown in the Quick Start section.

## Dependencies

Core Python dependencies (from `pyproject.toml`):

- `fastapi` — Modern, fast (high-performance) web framework for building APIs with Python
- `uvicorn[standard]` — ASGI server for running FastAPI apps (use `--reload` during development)
- `arq` >= 0.28.0 — Async job queue
- `label-studio-sdk` >= 2.1.0 — Label Studio integration
- `minio` >= 7.2.20 — MinIO client
- `psycopg2-binary` >= 2.9.12 — PostgreSQL adapter
- `pydantic` >= 2.13.4 — Data validation
- `pydantic-settings` >= 2.14.2 — Settings management
- `python-dotenv` >= 1.2.2 — Environment variable loading
- `sqlalchemy` >= 2.0.51 — ORM and database toolkit

Install dependencies with `uv sync` or `pip install -e .` as shown above (or `pip install fastapi uvicorn[standard]` to add the FastAPI runtime manually).

## Development Workflow

- Use the `sandbox/` folder for experiments and prototypes.
- Add reusable backend modules to `backend/` and import them into `main.py` as needed.
- Keep `diagrams/` updated when architecture changes.
- Use Docker Compose for running dependent services locally; prefer ephemeral volumes for experiments.

Common commands:

```bash
# Start services
docker compose -f compose.yml up -d

# Stream logs for a service
docker compose -f compose.yml logs -f label-studio

# Stop and remove services
docker compose -f compose.yml down
```

## Contributing

Contributions are welcome. Typical contribution workflow:

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests/examples as appropriate
4. Open a pull request describing the change and why it's useful

Please keep secrets out of commits and use `.env` or CI secrets for credentials.

## Contact

Maintainer: `jkznx`

For questions, feature requests, or contributions, please open an issue: https://github.com/jkznx/ai-ecosystem-workspace/issues
