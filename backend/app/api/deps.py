from collections.abc import Generator
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import UNAUTHORIZED, api_error
from app.core.security import decode_access_token
from app.domain.identity.entities import User
from app.infrastructure.db.session import SessionLocal

bearer = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if credentials is None:
        raise UNAUTHORIZED
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = UUID(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise UNAUTHORIZED
    user = db.get(User, user_id)
    if not user:
        raise api_error(401, "USER_NOT_FOUND", "The authenticated user no longer exists.")
    return user
