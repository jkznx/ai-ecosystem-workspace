# Scripts

Utility scripts for operating, testing, and maintaining the AI Ecosystem Workspace.

## Available scripts

- **export_openapi.py** - Export OpenAPI specification and API endpoint list (CSV, XLSX)
- **enqueue_job.py** - Helper to manually enqueue background jobs
- **upload_dataset.py** - Upload dataset files to MinIO object storage

## How to use

### Export OpenAPI and API documentation

```bash
python scripts/export_openapi.py
```

Generates:
- `docs/api/openapi.json` - Full OpenAPI 3.0 specification
- `docs/api/api-list.csv` - API endpoints in CSV format
- `docs/api/api-list.xlsx` - API endpoints in Excel format

Requirements: Backend must be running on `http://localhost:8000`

### Enqueue a background job

```bash
python scripts/enqueue_job.py
```

Interactively enqueues a job to the async queue.

Requirements: Redis running, backend configured

### Upload dataset to MinIO

```bash
python scripts/upload_dataset.py
```

Uploads a local dataset directory to MinIO for annotation/training.

Requirements: MinIO running, `.env` configured

## Running scripts

1. Activate the project environment:
   ```bash
   source .venv/bin/activate
   ```

2. Install dependencies (if not already done):
   ```bash
   pip install -e .
   ```

3. Run the script:
   ```bash
   python scripts/script_name.py
   ```

## Adding new scripts

1. Create a new `.py` file in `scripts/`
2. Add docstring explaining purpose and usage
3. Use command-line arguments or interactive prompts for configuration
4. Handle errors gracefully with informative messages
5. Test locally before committing

## Environment configuration

Scripts read from `.env` file (in project root):

```env
# Backend
BACKEND_URL=http://localhost:8000

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=ai-datasets

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Label Studio
LABELSTUDIO_URL=http://localhost:8080
LABELSTUDIO_API_KEY=your-key-here
```
