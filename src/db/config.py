import logging
from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

logger = logging.getLogger(__name__)
DATABASE_URL = settings.DATABASE_URL

# For SQLite only connect_args={"check_same_thread": False}
engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=settings.ECHO_SQL,
    pool_size=10,
    max_overflow=20,
)
SessionLocal = sessionmaker(
    engine, expire_on_commit=False, future=True, class_=AsyncSession
)


async def get_session() -> AsyncIterator[sessionmaker]:
    try:
        yield SessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)
