from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.api.deps import get_db, get_current_user
from backend.api.schemas.auth import Token, RefreshRequest, UserRead
from backend.core.db.models import User
from backend.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    return Token(**auth_service.login(db, form.username, form.password))


@router.post("/token/refresh", response_model=Token)
def refresh(body: RefreshRequest) -> Token:
    return Token(**auth_service.refresh(body.refresh_token))


@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)) -> User:
    return user