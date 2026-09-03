# Database (Core DB)

Database configuration, session management, and ORM models for the backend.

## Files

- **config.py** - Database connection configuration (from root `backend/core/config.py`)
- **session.py** - SQLAlchemy session factory and dependency injection
- **models.py** - SQLAlchemy ORM models (User, Student, Job, etc.)
- **test_students.py** - Example tests for student model queries

## How to use

### Initialize database session

```python
from backend.core.db.session import SessionLocal

db = SessionLocal()
try:
    # Use db session
    pass
finally:
    db.close()
```

### Use as dependency in FastAPI

```python
from fastapi import Depends
from backend.core.db.session import get_db
from sqlalchemy.orm import Session

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### Define models

```python
from sqlalchemy import Column, Integer, String
from backend.core.db.base import Base

class MyModel(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
```

## Database migrations

- Use Alembic for schema migrations (if configured)
- Place migration scripts in `alembic/versions/`
- Run migrations with `alembic upgrade head`
