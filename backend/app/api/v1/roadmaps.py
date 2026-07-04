from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.domain.identity.entities import User
from app.domain.roadmap.schemas import GenerateRoadmapRequest, RoadmapRead
from app.domain.roadmap.services import RoadmapService

router = APIRouter()


@router.post("/generate")
def generate(payload: GenerateRoadmapRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    roadmap = RoadmapService(db).generate(user, payload)
    return {"data": RoadmapRead.model_validate(roadmap).model_dump(mode="json"), "meta": {}, "errors": []}


@router.get("/current")
def current(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    roadmap = RoadmapService(db).current(user)
    return {"data": RoadmapRead.model_validate(roadmap).model_dump(mode="json") if roadmap else None, "meta": {}, "errors": []}
