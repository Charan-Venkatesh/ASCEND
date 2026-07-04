from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class DashboardSnapshot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "dashboard_snapshots"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
