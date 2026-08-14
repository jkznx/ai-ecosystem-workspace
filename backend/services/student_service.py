from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.db.models import Student


class StudentService:

    def list(self, db: Session, skip: int = 0, limit: int = 50) -> list[Student]:
        return list(db.scalars(select(Student).offset(skip).limit(limit)).all())

    def get(self, db: Session, student_id: int) -> Student | None:
        return db.get(Student, student_id)


student_service = StudentService()
