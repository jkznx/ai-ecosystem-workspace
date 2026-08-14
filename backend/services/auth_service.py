from sqlalchemy import select
from sqlalchemy.orm import Session

import jwt

from backend.core.db.models import User
from backend.core.exceptions import UnauthorizedError
from backend.core.security import (
    create_access_token, create_refresh_token, decode_token, verify_password,
)


class AuthService:
    def login(self, db: Session, username: str, password: str) -> dict:
        user = db.scalar(select(User).where(User.username == username))
        if user is None or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Incorrect username or password")
        return {
            "access_token": create_access_token(user.username),
            "refresh_token": create_refresh_token(user.username),
            "token_type": "bearer",
        }

    def refresh(self, refresh_token: str) -> dict:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise ValueError
        except (jwt.PyJWTError, ValueError) as e:
            raise UnauthorizedError("Invalid refresh token") from e

        username = payload["sub"]
        return {
            "access_token": create_access_token(username),
            "refresh_token": create_refresh_token(username),
            "token_type": "bearer",
        }


auth_service = AuthService()