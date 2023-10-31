from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey

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
    photo: str = Column(String(200), nullable=True)
    time: DateTime = Column(DateTime, nullable=False)
    owner: int = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
