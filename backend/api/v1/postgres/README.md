# PostgreSQL (Database) API

Endpoints for database health checks and schema information.

## Endpoints

- `GET /v1/postgres/health` - Database connection health
- `GET /v1/postgres/tables` - List tables in schema
- `GET /v1/postgres/tables/{table_name}/schema` - Get table schema

## How to use

```bash
# Check database health
curl http://localhost:8000/v1/postgres/health

# List tables
curl http://localhost:8000/v1/postgres/tables
```
