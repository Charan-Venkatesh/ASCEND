from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Mission(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "missions"

    roadmap_week_id: Mapped[UUID] = mapped_column(ForeignKey("roadmap_weeks.id", ondelete="CASCADE"), nullable=False)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    business_context: Mapped[str] = mapped_column(Text, nullable=False)
    learning_topic: Mapped[str] = mapped_column(String(220), nullable=False)
    practical_task: Mapped[str] = mapped_column(Text, nullable=False)
    documentation_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    reflection_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    interview_question: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=75, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="locked", nullable=False)
    unlocked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    week = relationship("RoadmapWeek", back_populates="missions")
    tasks = relationship("MissionTask", back_populates="mission", cascade="all, delete-orphan")
    evidence = relationship("MissionEvidence", back_populates="mission", cascade="all, delete-orphan")

    def complete(self) -> None:
        self.status = "completed"
        self.completed_at = datetime.now(UTC)


class MissionTask(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "mission_tasks"

    mission_id: Mapped[UUID] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    instructions: Mapped[str] = mapped_column(Text, nullable=False)
    skill_improved: Mapped[str] = mapped_column(String(140), nullable=False)
    completion_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)

    mission = relationship("Mission", back_populates="tasks")


class MissionEvidence(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "mission_evidence"

    mission_id: Mapped[UUID] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(40), nullable=False)
    reference_id: Mapped[UUID | None]
    url: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    mission = relationship("Mission", back_populates="evidence")
