from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_db
from app.domain.dashboard.entities import DashboardSnapshot
from app.domain.identity.entities import User
from app.domain.mission.schemas import MissionRead
from app.domain.mission.services import MissionService

router = APIRouter()


@router.get("/today")
def dashboard_today(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    snapshot = db.scalar(select(DashboardSnapshot).where(DashboardSnapshot.user_id == user.id))
    mission = MissionService(db).today(user)
    payload = snapshot.payload if snapshot else {"streak": 0, "completed_missions": 0, "skill_focus": ["Azure", "AI Architecture", "Automation"], "review_due": "Sunday"}
    payload["today_mission"] = MissionRead.model_validate(mission).model_dump(mode="json") if mission else None
    return {"data": payload, "meta": {}, "errors": []}
