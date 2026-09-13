# Label Studio API

Endpoints for integration with Label Studio data annotation platform.

## Endpoints

- `GET /v1/labelstudio/projects` - List annotation projects
- `GET /v1/labelstudio/projects/{project_id}/tasks` - List tasks in a project
- `GET /v1/labelstudio/projects/{project_id}/tasks/{task_id}/annotations` - Get annotations for a task
- `POST /v1/labelstudio/import` - Import dataset for annotation
- `POST /v1/labelstudio/export` - Export annotated data

## How to use

```bash
# List projects
curl http://localhost:8000/v1/labelstudio/projects

# Get project tasks
curl http://localhost:8000/v1/labelstudio/projects/{project_id}/tasks
```

## Configuration

Set Label Studio connection details in `.env`:
```
LABELSTUDIO_URL=http://localhost:8080
LABELSTUDIO_API_KEY=your-api-key
```

## Integration

Label Studio client is initialized in `backend/libs/labelstudio_client.py`.
Endpoints use this client to communicate with Label Studio.
