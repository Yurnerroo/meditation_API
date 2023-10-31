from sqlalchemy import Column, Integer, String, DateTime, func

from .base import Base


class Exercise(Base):
    __tablename__ = "exercises"
    id: int = Column(
        "id",
        Integer,
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        index=True,
    )
    text: str = Column(String(1000), nullable=False)
    photo: str = Column(String(200), nullable=False)
    time: DateTime = Column(DateTime, nullable=False, server_default=func.now())
