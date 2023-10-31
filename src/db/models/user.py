from __future__ import annotations

import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
)

from .base import Base


class UserTypesEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


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
    name: str = Column(String(25), unique=True, index=True, nullable=False)
    avatar: str = Column(String(150), nullable=True)
    user_type: Enum = Column(Enum(UserTypesEnum), default=UserTypesEnum.USER)
    password_hash: str = Column(String(60), nullable=False)
