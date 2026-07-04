from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(512))
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    auth_provider: Mapped[str] = mapped_column(String(32), default="email", nullable=False)

    profile = relationship("CareerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
