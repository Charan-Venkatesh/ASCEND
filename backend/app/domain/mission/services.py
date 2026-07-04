from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.exceptions import api_error
from app.domain.identity.entities import User
from app.domain.mission.entities import Mission, MissionEvidence, MissionTask
from app.domain.mission.schemas import EvidenceRequest
from app.domain.roadmap.entities import Roadmap, RoadmapWeek
from app.infrastructure.queue.events import EventBus


class MissionService:
    def __init__(self, db: Session, event_bus: EventBus | None = None) -> None:
        self.db = db
        self.event_bus = event_bus or EventBus()

    def today(self, user: User) -> Mission | None:
        return self.db.scalar(
            select(Mission)
            .join(RoadmapWeek)
            .join(Roadmap)
            .where(Roadmap.user_id == user.id, Roadmap.status == "active", Mission.status.in_(["available", "in_progress"]))
            .options(selectinload(Mission.tasks), selectinload(Mission.evidence))
            .order_by(Mission.day_number)
            .limit(1)
        )

    def get_for_user(self, user: User, mission_id: UUID) -> Mission:
        mission = self.db.scalar(
            select(Mission)
            .join(RoadmapWeek)
            .join(Roadmap)
            .where(Roadmap.user_id == user.id, Mission.id == mission_id)
            .options(selectinload(Mission.tasks), selectinload(Mission.evidence))
        )
        if not mission:
            raise api_error(404, "MISSION_NOT_FOUND", "Mission was not found.")
        return mission

    def add_evidence(self, user: User, mission_id: UUID, payload: EvidenceRequest) -> MissionEvidence:
        mission = self.get_for_user(user, mission_id)
        if mission.status == "locked":
            raise api_error(423, "MISSION_LOCKED", "Complete the current mission before opening this one.")
        evidence = MissionEvidence(mission_id=mission.id, user_id=user.id, evidence_type=payload.evidence_type, url=payload.url, summary=payload.summary)
        self.db.add(evidence)
        if mission.status == "available":
            mission.status = "in_progress"
        self.db.commit()
        self.db.refresh(evidence)
        return evidence

    def complete_task(self, user: User, mission_id: UUID, task_id: UUID) -> Mission:
        mission = self.get_for_user(user, mission_id)
        task = next((item for item in mission.tasks if item.id == task_id), None)
        if not task:
            raise api_error(404, "TASK_NOT_FOUND", "Mission task was not found.")
        task.status = "completed"
        if mission.status == "available":
            mission.status = "in_progress"
        self.db.commit()
        return self.get_for_user(user, mission_id)

    def complete(self, user: User, mission_id: UUID) -> Mission:
        mission = self.get_for_user(user, mission_id)
        if mission.status == "locked":
            raise api_error(423, "MISSION_LOCKED", "This mission is locked.")
        if not mission.evidence:
            raise api_error(422, "EVIDENCE_REQUIRED", "Attach evidence before completing the mission.")
        mission.complete()
        next_mission = self.db.scalar(
            select(Mission)
            .join(RoadmapWeek)
            .join(Roadmap)
            .where(Roadmap.user_id == user.id, Roadmap.status == "active", Mission.day_number == mission.day_number + 1)
        )
        if next_mission and next_mission.status == "locked":
            next_mission.status = "available"
            next_mission.unlocked_at = datetime.now(UTC)
        self.db.commit()
        self.event_bus.publish("ascend.domain.events", "mission.completed", {"user_id": user.id, "mission_id": mission.id, "day_number": mission.day_number, "completed_at": mission.completed_at})
        return self.get_for_user(user, mission_id)
