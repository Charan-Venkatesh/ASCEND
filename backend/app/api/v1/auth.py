from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.domain.identity.entities import User
from app.domain.identity.schemas import LoginRequest, RegisterRequest, TokenResponse, UserRead
from app.domain.identity.services import IdentityService

router = APIRouter()


@router.post("/register", response_model=dict)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> dict:
    token = IdentityService(db).register(payload)
    return {"data": token.model_dump(mode="json"), "meta": {}, "errors": []}


@router.post("/login", response_model=dict)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    token = IdentityService(db).login(payload)
    return {"data": token.model_dump(mode="json"), "meta": {}, "errors": []}


@router.get("/me", response_model=dict)
def me(user: User = Depends(get_current_user)) -> dict:
    return {"data": UserRead.model_validate(user).model_dump(mode="json"), "meta": {}, "errors": []}
