from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
import jwt

from backend.api.deps import get_db, get_current_user
from backend.api.schemas import Token, RefreshRequest, UserRead
from backend.core.db.models import User
from backend.core.security import verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = db.scalar(select(User).where(User.username == form.username))
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return Token(
        access_token=create_access_token(user.username),
        refresh_token=create_refresh_token(user.username),
    )

@router.post("/token/refresh", response_model=Token)
def refresh(body: RefreshRequest) -> Token:
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    username = payload["sub"]
    return Token(
        access_token=create_access_token(username),
        refresh_token=create_refresh_token(username),
    )

@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)) -> User:
    return user