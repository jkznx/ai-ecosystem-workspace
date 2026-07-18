from sqlalchemy import select
from backend.core.db.models import Student
from backend.core.db.session import Base, engine, get_session


def create_table():
    Base.metadata.create_all(bind=engine, tables=[Student.__table__])


def insert_data():
    with get_session() as s:
        s.add_all([
            Student(name="Alice Johnson", age=21, major="Computer Science"),
            Student(name="Bob Smith", age=22, major="Mathematics"),
            Student(name="Carol Lee", age=20, major="Physics"),
        ])
        s.commit()


def read_data():
    with get_session() as s:
        for row in s.scalars(select(Student)).all():
            print(row)


def update_data():
    with get_session() as s:
        st = s.scalars(select(Student).where(Student.name == "Bob Smith")).first()
        if st:
            st.major = "Data Science"
            s.commit()


def delete_data():
    with get_session() as s:
        st = s.scalars(select(Student).where(Student.name == "Carol Lee")).first()
        if st:
            s.delete(st)
            s.commit()


def drop_table():
    Base.metadata.drop_all(bind=engine, tables=[Student.__table__])


if __name__ == "__main__":
    create_table()
    insert_data()
    read_data()
    update_data()
    read_data()
    delete_data()
    read_data()
    drop_table()