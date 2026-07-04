from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CareerProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "career_profiles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    current_role: Mapped[str] = mapped_column(String(160), default="IT Operations Engineer", nullable=False)
    target_role: Mapped[str] = mapped_column(String(160), default="Enterprise AI & Cloud Architect", nullable=False)
    learning_style: Mapped[str] = mapped_column(String(80), default="step_by_step", nullable=False)
    target_company: Mapped[str | None] = mapped_column(String(160))
    target_salary: Mapped[Decimal | None] = mapped_column(Numeric())
    preferred_daily_minutes: Mapped[int] = mapped_column(Integer, default=75, nullable=False)
    mentor_tone: Mapped[str] = mapped_column(String(40), default="friendly", nullable=False)

    user = relationship("User", back_populates="profile")
