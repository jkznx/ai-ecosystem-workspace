# AI Ecosystem Workspace

A modular workspace for developing, experimenting, and integrating AI tools, models, and pipelines. This project provides a containerized environment with essential services and infrastructure for AI development.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Services](#services)
- [Dependencies](#dependencies)
- [Contact](#contact)

## Overview

AI Ecosystem Workspace is designed as a lightweight, composable platform for AI experimentation and integration. It uses Docker Compose to orchestrate services and includes Python tooling for data processing, model training, and API interactions.

**Key Features:**
- Multi-service Docker Compose setup
- Label Studio for data annotation
- MinIO for S3-compatible object storage
- PostgreSQL database backend
- Redis for caching and async task queues
- Python 3.14+ with modern dependency management

## Project Structure

```
ai-ecosystem-workspace/
├── README.md              # This file
├── compose.yml            # Docker Compose services configuration
├── pyproject.toml         # Python project metadata and dependencies
├── main.py                # Main entry point
├── .python-version        # Python version specification
├── uv.lock                # Locked dependencies
├── backend/               # Backend application code (placeholder)
├── sandbox/               # Experimentation and prototyping area
├── diagrams/              # Architecture and documentation diagrams
└── out.jpg                # Generated output/visualization
```

## Getting Started

### Prerequisites

- **Git** (latest stable)
- **Docker & Docker Compose** (for running services)
- **Python 3.14+** (for local development)
- **uv** (recommended) or **pip** (for dependency management)

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/jkznx/ai-ecosystem-workspace.git
cd ai-ecosystem-workspace
```

#### 2. Set Up Python Environment

Using **uv** (recommended):
```bash
uv sync
```

Or using **venv**:
```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.\.venv\Scripts\activate     # Windows (PowerShell)
pip install -e .
```

#### 3. Start Docker Services

Bring up all services with Docker Compose:

```bash
docker compose up -d
```

This will start:
- **Redis** (port 6379) — Caching and async job queue
- **PostgreSQL** (port 5433) — Database backend
- **Label Studio** (port 8080) — Data annotation tool
- **MinIO** (ports 9000, 9001) — S3-compatible object storage

#### 4. Run the Application

```bash
python main.py
```

## Services

### Redis
- **Image:** `redis:8.8.0-alpine`
- **Port:** 6379
- **Purpose:** Caching, async task queues (with arq)
- **Persistence:** Enabled with AOF (append-only file)

### PostgreSQL
- **Image:** `postgres:16-alpine`
- **Port:** 5433 (mapped from 5432)
- **Credentials:** 
  - User: `postgres`
  - Password: `postgres`
  - Database: `label_studio`

### Label Studio
- **Image:** `heartexlabs/label-studio:latest`
- **Port:** 8080
- **Purpose:** Data labeling and annotation interface
- **Database:** Connected to PostgreSQL

### MinIO
- **Image:** `minio/minio:latest`
- **Ports:** 
  - 9000 (S3 API)
  - 9001 (Web console)
- **Purpose:** Object storage (S3-compatible)
- **Credentials:**
  - Access Key: `minioadmin`
  - Secret Key: `aegis@810vii`

## Dependencies

Core Python dependencies (from `pyproject.toml`):

- **arq** ≥0.28.0 — Async job queue
- **label-studio-sdk** ≥2.1.0 — Label Studio integration
- **minio** ≥7.2.20 — MinIO client
- **psycopg2-binary** ≥2.9.12 — PostgreSQL adapter
- **pydantic** ≥2.13.4 — Data validation
- **pydantic-settings** ≥2.14.2 — Settings management
- **python-dotenv** ≥1.2.2 — Environment variable loading
- **sqlalchemy** ≥2.0.51 — ORM and database toolkit

Install all dependencies with:
```bash
uv sync
# or
pip install -e .
```

## Development Workflow

### Local Development

1. Activate the Python environment
2. Use `sandbox/` for experimentation
3. Add new backend modules to `backend/`
4. Keep `diagrams/` updated with architecture changes

### Running Services in Development

```bash
# Start services in the background
docker compose up -d

# View logs
docker compose logs -f label-studio

# Stop services
docker compose down
```

## Contact

**Maintainer:** jkznx

For questions, feature requests, or contributions, please [open an issue](https://github.com/jkznx/ai-ecosystem-workspace/issues) in this repository.
