import enum

from sqlalchemy import Column, Integer, DateTime, func, String, ForeignKey, Enum

from .base import Base


class PostStatusesEnum(str, enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    WAITING = "waiting for review"


class Post(Base):
    __tablename__ = "posts"
    id: int = Column(
        "id",
        Integer,
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        index=True,
    )
    title: str = Column(String(150), nullable=False)
    description: str = Column(String(1000), nullable=True)
    time: DateTime = Column(DateTime, nullable=False, server_default=func.now())
    photo: str = Column(String(500), nullable=True)
    owner: int = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status: Enum = Column(Enum(PostStatusesEnum), default=PostStatusesEnum.WAITING)
