from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
    func,
)

from .base import Base


class User(Base):
    __tablename__ = "users"
    id: int = Column(
        "id",
        Integer,
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        index=True,
    )
    username: str = Column(String(25), unique=True, index=True, nullable=False)
    password_hash: str = Column(String(60), nullable=False)
    full_name: str = Column(String(50), nullable=False)
    email: str = Column(String(254), nullable=False)
    is_super_user: bool = Column(Boolean, nullable=False, default=False)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    date_joined: DateTime = Column(DateTime, nullable=False, server_default=func.now())
    is_approved: bool = Column(Boolean, nullable=False, default=False)
    created_by_user_id: int = Column(Integer, nullable=True)

    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)
