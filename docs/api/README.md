# API Documentation

Generated and exported API documentation for the backend.

## Files

- **openapi.json** - OpenAPI 3.0 specification (auto-generated from FastAPI)
- **api-list.csv** - Exported API endpoints in CSV format
- **api-list.xlsx** - Exported API endpoints in Excel format

## How to update

Run the export script to regenerate OpenAPI and endpoint lists:

```bash
python scripts/export_openapi.py
```

This command:
1. Starts the backend API
2. Fetches OpenAPI schema from `/openapi.json`
3. Exports endpoints to CSV and XLSX formats
4. Saves files to `docs/api/`

## Viewing API docs

When backend is running:
- Interactive Swagger UI: `http://localhost:8000/docs`
- ReDoc API documentation: `http://localhost:8000/redoc`
- Raw OpenAPI JSON: `http://localhost:8000/openapi.json`

## OpenAPI schema

The OpenAPI schema is automatically generated from:
- FastAPI route definitions
- Pydantic model schemas
- Response models
- Parameter documentation

No manual schema updates needed; regenerate with `export_openapi.py` after API changes.
