from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from backend.core.db.session import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    major: Mapped[str] = mapped_column(String(120), nullable=False)

    def __repr__(self):
        return f"Student(id={self.id}, name={self.name!r}, age={self.age}, major={self.major!r})"