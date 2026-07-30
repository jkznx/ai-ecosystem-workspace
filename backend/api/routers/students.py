from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.api.deps import get_db, get_current_user
from backend.api.schemas import StudentRead
from backend.core.db.models import Student, User

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=list[StudentRead])
def list_students(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Student]:
    return list(db.scalars(select(Student).offset(skip).limit(limit)).all())
