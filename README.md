<p align="center">
  <img src="baby.png" alt="logo" width="160" style="border-radius:12px; box-shadow: 0 8px 24px rgba(33,37,41,0.12);"/>
</p>

# AI Ecosystem Workspace

A modular workspace for developing, experimenting, and integrating AI tools, models, and pipelines. This repository provides developer tooling, Python backend code, diagrams, utility scripts, and sandboxed integrations for experimentation.

## Table of Contents

- [Overview](#overview)
- [Current repository state](#current-repository-state)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment & Dependencies](#environment--dependencies)
- [Services (Docker Compose)](#services-docker-compose)
- [FastAPI Example](#fastapi-example)
- [Development Workflow](#development-workflow)
- [What changed recently](#what-changed-recently)
- [Contributing](#contributing)
- [Contact](#contact)

## Overview

AI Ecosystem Workspace is designed as a lightweight, composable platform for AI experimentation and integration. It includes a small Python backend, scripts to help with OpenAPI export and job enqueueing, sandboxed integrations (Label Studio, MinIO), and architecture diagrams.

Use this repository as a local developer playground for model prototyping, data labeling workflows, and integration experiments.

## Current repository state

This update reflects the repository's current state as of the latest commit:
- Component-level README.md files have been added under backend/, diagrams/, docs/, scripts/, and sandbox/ to document the current state and usage notes for each area.
- The backend entry point exists at `backend/main.py` and the repository root contains `main.py` (example entry script).
- Utility scripts are available under `scripts/` (for exporting OpenAPI and enqueueing jobs).
- Diagrams source (`diagrams/overview.dio`) and image (`diagrams/overview.png`) are present.

See the `What changed recently` section below for commit links and summary.

## Project Structure

[![GitHubTree](https://img.shields.io/badge/Structure-GitHubTree-blue?style=flat-square)](https://githubtree.mgks.dev/repo/jkznx/ai-ecosystem-workspace/main/)

```
ai-ecosystem-workspace/
├── README.md           # This file
├── compose.yml           # Docker Compose services configuration
├── pyproject.toml        # Python project metadata and dependencies
├── main.py               # Example entry or script at repository root
├── backend/              # Backend application code
│   ├── main.py           # Backend entry point
│   ├── api/              # HTTP API (endpoints)
│   ├── core/             # Core business logic and models
│   ├── libs/             # Internal libraries and utilities
│   ├── services/         # Service layer and integrations
│   ├── utils/            # Helper utilities
│   └── workers/          # Background worker implementations
├── scripts/              # Utility scripts (export_openapi.py, enqueue_job.py)
├── docs/                 # Documentation artifacts and API exports
├── diagrams/             # Architecture diagrams (source + PNG)
├── sandbox/              # Experimental integrations (labelstudio, minio)
└── out.jpg               # Example generated output / visualization
```

## Getting Started

### Prerequisites

- Git
- Docker & Docker Compose (for running services)
- Python 3.14+ (see `.python-version`)
- `uv` (optional) or pip for dependency management

### Quick Start (local development)

1. Clone the repository

```bash
git clone https://github.com/jkznx/ai-ecosystem-workspace.git
cd ai-ecosystem-workspace
```

2. Create a Python virtual environment and install the project

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
# or .\.venv\Scripts\activate on Windows (PowerShell)
pip install -e .
```

(If you use `uv`, run `uv sync` to apply the lockfile.)

3. Start dependent services with Docker Compose (optional)

```bash
docker compose -f compose.yml up -d
```

4. Run the backend example

```bash
python backend/main.py
```

Or run a FastAPI app (if present) with Uvicorn:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment & Dependencies

- `.python-version` contains the target Python version for the project.
- `pyproject.toml` lists the Python dependencies. Use `pip install -e .` or `uv sync` (if using `uv`) to install.

Common runtime dependencies used or expected by the repository include FastAPI, Uvicorn, arq (async queue), MinIO client, psycopg2, SQLAlchemy, and pydantic.

## Services (Docker Compose)

The repository includes `compose.yml` to start common development services for the workspace. Typical services include:
- Redis (caching and async queue backend)
- PostgreSQL (relational database for examples and Label Studio)
- Label Studio (annotation interface)
- MinIO (S3-compatible object storage)

Use a `.env` file to override default credentials and ports before starting the compose stack.

## FastAPI Example

A minimal FastAPI example is recommended and can be placed at `backend/app/main.py`. It should expose a `/health` and sample `/hello` endpoint and can be run with Uvicorn to view interactive docs at `/docs`.

## Development Workflow

- Use `sandbox/` for experiments and prototypes. Don't rely on sandbox artifacts for production code.
- Add stable, reusable code to `backend/` and keep component READMEs up-to-date.
- Update `diagrams/` when architecture changes.
- Keep secrets out of the repository. Use `.env` in development and a secure secrets manager for shared/production deployments.

Common commands:

```bash
# Start services
docker compose -f compose.yml up -d

# Tail logs for a service
docker compose -f compose.yml logs -f label-studio

# Stop and remove services
docker compose -f compose.yml down
```

## What changed recently

- Component README files were added to document the current state of backend subpackages, diagrams, docs, scripts, and sandbox.
- Commit: Add README.md files for components to document current state
  - https://github.com/jkznx/ai-ecosystem-workspace/commit/158251a7b05f201b22e4326972b2e70db161d6b7

If you want a full CHANGELOG or versioned releases, consider adding a `CHANGELOG.md` and tagging releases.

## Contributing

Contributions are welcome. Typical workflow:

1. Fork and clone
2. Create a feature branch
3. Add changes and tests
4. Open a pull request describing the change

Please avoid committing secrets. Use `.env` files for local development and CI secrets for automation.

## Contact

Maintainer: `jkznx`

Open an issue for questions or requests: https://github.com/jkznx/ai-ecosystem-workspace/issues
