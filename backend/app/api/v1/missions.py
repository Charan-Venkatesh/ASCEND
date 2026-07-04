from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.domain.identity.entities import User
from app.domain.mission.schemas import EvidenceRequest, MissionRead
from app.domain.mission.services import MissionService

router = APIRouter()


@router.get("/today")
def today(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    mission = MissionService(db).today(user)
    return {"data": MissionRead.model_validate(mission).model_dump(mode="json") if mission else None, "meta": {}, "errors": []}


@router.get("/{mission_id}")
def get_mission(mission_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    mission = MissionService(db).get_for_user(user, mission_id)
    return {"data": MissionRead.model_validate(mission).model_dump(mode="json"), "meta": {}, "errors": []}


@router.post("/{mission_id}/tasks/{task_id}/complete")
def complete_task(mission_id: UUID, task_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    mission = MissionService(db).complete_task(user, mission_id, task_id)
    return {"data": MissionRead.model_validate(mission).model_dump(mode="json"), "meta": {}, "errors": []}


@router.post("/{mission_id}/evidence")
def add_evidence(mission_id: UUID, payload: EvidenceRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    evidence = MissionService(db).add_evidence(user, mission_id, payload)
    return {"data": {"id": str(evidence.id), "summary": evidence.summary}, "meta": {}, "errors": []}


@router.post("/{mission_id}/complete")
def complete_mission(mission_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    mission = MissionService(db).complete(user, mission_id)
    return {"data": MissionRead.model_validate(mission).model_dump(mode="json"), "meta": {}, "errors": []}
