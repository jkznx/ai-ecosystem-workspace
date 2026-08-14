# Backend

This directory contains the Python backend for the AI ecosystem workspace.

Current state:
- main.py: entry point for running the backend.
- Subpackages: api, core, libs, services, utils, workers (each may be a namespace package or contain modules).

How to run (local/development):
1. Create a virtual environment and install dependencies (see project pyproject.toml):
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .

2. Run the backend entry point:
   python backend/main.py

Notes / next steps:
- The backend is split into subpackages; add README files inside each subpackage (already present) to document public APIs and configuration for that area.
- If you plan to run via Docker/Compose, check compose.yml at the repository root.
