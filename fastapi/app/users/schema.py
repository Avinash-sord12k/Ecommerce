from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String(255), unique=True, nullable=False)
    password: str = Column(String(255), nullable=False)
    email: str = Column(String(255), unique=True, nullable=True)
    full_name: str = Column(String(255), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    phone: str = Column(String(255), nullable=True)
    address: str = Column(String(255), nullable=True)
    created_at: datetime = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    is_internal_user: bool = Column(Boolean, default=False)
    date_joined: datetime = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    last_active: datetime = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    role = relationship("Role", back_populates="users")
