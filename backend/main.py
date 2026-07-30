from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from backend.api.routers import health, students, storage, annotation, jobs, auth
from backend.core.config import settings
from backend.core.db.session import Base, engine, get_session
from backend.core.db.models import User
from backend.core.logger import logger
from backend.core.security import hash_password

def _seed_admin() -> None:
    with get_session() as db:
        exists = db.scalar(select(User).where(User.username == settings.ADMIN_USERNAME))
        if exists is None:
            db.add(User(
                username=settings.ADMIN_USERNAME,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                is_admin=True,
            ))
            db.commit()
            logger.info("Seeded default admin user %r", settings.ADMIN_USERNAME)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up %s", settings.APP_NAME)
    Base.metadata.create_all(bind=engine)
    _seed_admin()
    yield
    logger.info("Shutting down %s", settings.APP_NAME)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(students.router, prefix="/api/v1")
app.include_router(storage.router, prefix="/api/v1")
app.include_router(annotation.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")