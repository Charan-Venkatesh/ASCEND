from datetime import date
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Roadmap(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "roadmaps"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, default=180, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    generated_by: Mapped[str] = mapped_column(String(32), default="template", nullable=False)
    started_at: Mapped[date | None] = mapped_column(Date)

    weeks = relationship("RoadmapWeek", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapWeek.week_number")


class RoadmapWeek(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "roadmap_weeks"

    roadmap_id: Mapped[UUID] = mapped_column(ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False)
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    theme: Mapped[str] = mapped_column(String(220), nullable=False)
    objectives: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    roadmap = relationship("Roadmap", back_populates="weeks")
    missions = relationship("Mission", back_populates="week", cascade="all, delete-orphan", order_by="Mission.day_number")
