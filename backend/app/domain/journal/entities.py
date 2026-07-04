from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class JournalEntry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "journal_entries"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mission_id: Mapped[UUID | None] = mapped_column(ForeignKey("missions.id", ondelete="SET NULL"))
    entry_date: Mapped[date] = mapped_column(Date, nullable=False)
    wins: Mapped[str | None] = mapped_column(Text)
    failures: Mapped[str | None] = mapped_column(Text)
    lessons_learned: Mapped[str | None] = mapped_column(Text)
    root_cause: Mapped[str | None] = mapped_column(Text)
    automation_ideas: Mapped[str | None] = mapped_column(Text)
    reflection: Mapped[str] = mapped_column(Text, nullable=False)
