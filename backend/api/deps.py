from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from collections.abc import Generator
from sqlalchemy import select
from sqlalchemy.orm import Session
import jwt

from backend.core.db.models import User
from backend.core.db.session import get_session
from backend.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db() -> Generator[Session, None, None]:
    with get_session() as session:
        yield session
        
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise credentials_error
        username = payload.get("sub")
    except jwt.PyJWTError:
        raise credentials_error

    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        raise credentials_error
    return user

def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user