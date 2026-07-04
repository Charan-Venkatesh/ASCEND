from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.domain.identity.entities import User
from app.domain.mission.entities import Mission, MissionTask
from app.domain.roadmap.entities import Roadmap, RoadmapWeek
from app.domain.roadmap.schemas import GenerateRoadmapRequest


TRACK = [
    ("Cloud foundations", "Azure identity, networking, governance"),
    ("Automation discipline", "PowerShell, Python, IaC, runbooks"),
    ("AI platform foundations", "LLMs, RAG, vector stores, orchestration"),
    ("Enterprise architecture", "Security, reliability, cost, landing zones"),
    ("Portfolio delivery", "Architectural documentation and executive communication"),
]


class RoadmapService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def current(self, user: User) -> Roadmap | None:
        return self.db.scalar(select(Roadmap).where(Roadmap.user_id == user.id, Roadmap.status == "active").options(selectinload(Roadmap.weeks).selectinload(RoadmapWeek.missions)))

    def generate(self, user: User, payload: GenerateRoadmapRequest) -> Roadmap:
        existing = self.current(user)
        if existing:
            return existing
        roadmap = Roadmap(user_id=user.id, title=f"180-Day {payload.target_role}", duration_days=180, status="active", generated_by="template", started_at=date.today())
        self.db.add(roadmap)
        self.db.flush()
        for week_number in range(1, 27):
            theme, objective = TRACK[(week_number - 1) % len(TRACK)]
            week = RoadmapWeek(roadmap_id=roadmap.id, week_number=week_number, theme=f"Week {week_number}: {theme}", objectives=[objective], is_locked=week_number != 1)
            self.db.add(week)
            self.db.flush()
            for day in range(1, 8):
                day_number = ((week_number - 1) * 7) + day
                if day_number > 180:
                    break
                status = "available" if day_number == 1 else "locked"
                mission = Mission(
                    roadmap_week_id=week.id,
                    day_number=day_number,
                    title=f"Day {day_number}: {theme} execution block",
                    objective=f"Build practical confidence in {objective}.",
                    business_context=f"Architects are trusted when they connect {theme.lower()} to reliable business outcomes.",
                    learning_topic=objective,
                    practical_task=f"Complete a focused lab or design note for {objective}; capture commands, decisions, and tradeoffs.",
                    documentation_prompt="Write evidence that a reviewer could use to understand what you did, why it mattered, and what changed.",
                    reflection_prompt="What assumption did you test today, what failed, and what will you do differently tomorrow?",
                    interview_question=f"Explain how you would apply {objective} in an enterprise production incident or design review.",
                    difficulty=min(5, 1 + (week_number // 6)),
                    estimated_minutes=payload.preferred_daily_minutes,
                    status=status,
                    unlocked_at=datetime.now(UTC) if status == "available" else None,
                )
                self.db.add(mission)
                self.db.flush()
                for task_type, title in [("learning", "Study"), ("lab", "Execute"), ("docs", "Document"), ("reflection", "Reflect"), ("interview", "Answer")]:
                    self.db.add(MissionTask(mission_id=mission.id, type=task_type, title=f"{title}: {objective}", instructions=f"{title} the mission topic with concrete evidence.", skill_improved=theme, completion_criteria="Evidence is specific, reviewable, and linked to the mission.", status="pending"))
        self.db.commit()
        self.db.refresh(roadmap)
        return roadmap
