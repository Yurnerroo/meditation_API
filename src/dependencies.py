from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from db.config import get_session
from db.crud.user_crud import UserCrud


async def get_user_crud(async_session: sessionmaker = Depends(get_session)):
    async with async_session() as session:
        async with session.begin():
            yield UserCrud(session)
