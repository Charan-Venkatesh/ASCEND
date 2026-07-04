from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.domain.identity.entities import User
from app.domain.mentor.services import AIOrchestrator

router = APIRouter()


class MentorChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    mode: str = "mentor"


@router.post("/chat")
def mentor_chat(payload: MentorChatRequest, user: User = Depends(get_current_user)) -> dict:
    answer = AIOrchestrator().mentor_chat(user.id, payload.message, payload.mode)
    return {"data": {"answer": answer}, "meta": {}, "errors": []}
