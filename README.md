<p align="center">
  <img src="dev\github\logo\baby.png" alt="logo" width="160" style="border-radius:12px; box-shadow: 0 8px 24px rgba(33,37,41,0.12);"/>
</p>

# AI Ecosystem Workspace

A lightweight, composable platform for AI experimentation and integration — now with a friendlier presentation and a logo at the top.

---

<p align="center">
  <strong style="font-size:1.15rem; color:#0f172a;">Modular tools, fast prototyping, and clear examples for AI integrations.</strong>
</p>

## Quick links

- ⚙️ Features: modular backend, worker queue examples, sandbox integrations
- 🚀 Run: local Docker Compose + FastAPI example
- 🧪 Use sandbox/ for experiments; move stable code to backend/

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment & Dependencies](#environment--dependencies)
- [Services (Docker Compose)](#services-docker-compose)
- [Development Workflow](#development-workflow)
- [Contributing](#contributing)

---

## Overview

AI Ecosystem Workspace is designed as a developer playground for model prototyping, data labeling workflows, and integration experiments. It contains a small Python backend, utility scripts, diagrams, and sandbox integrations to help you iterate quickly.

## Project Structure

[![GitHubTree](https://img.shields.io/badge/GitHubTree-ai--ecosystem--workspace-blue?style=flat-square)](https://githubtree.mgks.dev/repo/jkznx/ai-ecosystem-workspace/main/?ref=badge)

## Getting Started

### Prerequisites

- Git
- Docker & Docker Compose (optional, for services)
- Python 3.14+ (see `.python-version`)

### Quick start

```bash
git clone https://github.com/jkznx/ai-ecosystem-workspace.git
cd ai-ecosystem-workspace
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
pip install -e .
```

Start optional services with Docker Compose:

```bash
docker compose -f compose.yml up -d
```

Run the backend example:

```bash
python backend/main.py
# or with Uvicorn for a FastAPI app
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment & Dependencies

See `pyproject.toml` for dependencies. Common runtime packages include FastAPI, Uvicorn, arq, MinIO client, psycopg2, SQLAlchemy, and pydantic.

## Development Workflow

- Use `sandbox/` for experiments. Keep production-ready code in `backend/`.
- Keep secrets out of the repository. Use `.env` locally and a secrets manager in production.

Common commands:

```bash
# Start dev services
docker compose -f compose.yml up -d

# Tail logs
docker compose -f compose.yml logs -f label-studio

# Stop services
docker compose -f compose.yml down
```

## Contributing

Fork, create a feature branch, add tests, and open a pull request. Please avoid committing secrets.

## Contact

Maintainer: `jkznx`
Open an issue: https://github.com/jkznx/ai-ecosystem-workspace/issues
