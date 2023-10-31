from sqlalchemy.ext.asyncio import AsyncSession

from db.config import SessionLocal
from db.init import populators as p


async def init_db() -> None:
    session: AsyncSession
    async with SessionLocal() as session:
        async with session.begin():
            await p.populate_users(session=session)
