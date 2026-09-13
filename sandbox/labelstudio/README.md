# Label Studio Sandbox

Experimental Label Studio integration scripts and utilities.

## Scripts

- **list_projects.py** - List all annotation projects in Label Studio
- **list_tasks.py** - List tasks within a project

## How to use

```bash
# List Label Studio projects
python sandbox/labelstudio/list_projects.py

# List tasks in a project
python sandbox/labelstudio/list_tasks.py
```

## Configuration

Set Label Studio connection details in `.env` or environment:
```
LABELSTUDIO_URL=http://localhost:8080
LABELSTUDIO_API_KEY=your-api-key
```

## Notes

- These are sandbox/experimental scripts; use production code from `backend/`
- Connection tested against Label Studio running in Docker Compose
- See `compose.yml` for Label Studio service configuration
