from sqlalchemy.orm import Session

from app.core.exceptions import api_error
from app.core.security import create_access_token, hash_password, verify_password
from app.domain.identity.entities import User
from app.domain.identity.repositories import UserRepository
from app.domain.identity.schemas import LoginRequest, RegisterRequest, TokenResponse


class IdentityService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def register(self, payload: RegisterRequest) -> TokenResponse:
        if self.users.by_email(str(payload.email)):
            raise api_error(409, "EMAIL_EXISTS", "An account with this email already exists.")
        user = self.users.add(User(email=str(payload.email).lower(), display_name=payload.display_name, password_hash=hash_password(payload.password)))
        self.db.commit()
        self.db.refresh(user)
        return TokenResponse(access_token=create_access_token(user.id, user.email), user=user)

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self.users.by_email(str(payload.email))
        if not user or not verify_password(payload.password, user.password_hash):
            raise api_error(401, "INVALID_CREDENTIALS", "Email or password is incorrect.")
        return TokenResponse(access_token=create_access_token(user.id, user.email), user=user)
