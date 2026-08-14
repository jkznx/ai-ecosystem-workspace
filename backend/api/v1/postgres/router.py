from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.deps import get_current_user, get_db
from backend.api.schemas.postgres import StudentRead
from backend.core.db.models import User
from backend.services.student_service import student_service

router = APIRouter(prefix="/postgres", tags=["postgres"])


# ---- load: read only ----
@router.get("/load/students", response_model=list[StudentRead])
def load_students(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[StudentRead]:
    return student_service.list(db, skip=skip, limit=limit)
