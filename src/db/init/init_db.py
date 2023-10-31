from sqlalchemy.ext.asyncio import AsyncSession

from db.config import SessionLocal
from db.init import populators as p


async def init_db() -> None:
    session: AsyncSession
    async with SessionLocal() as session:
        async with session.begin():
            await p.populate_groups(session=session)
            await p.populate_users(session=session)
            total_perm = await p.populate_permissions(session=session)
            await p.populate_groups_permission(
                session=session, total_permissions=total_perm
            )
            await p.populate_users_groups(session=session)
