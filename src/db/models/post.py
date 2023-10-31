from sqlalchemy import Column, Integer, DateTime, func, String, ForeignKey

from .base import Base


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
    time: DateTime = Column(DateTime, nullable=False, server_default=func.now())
    photo: str = Column(String(500), nullable=True)
    owner: int = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
