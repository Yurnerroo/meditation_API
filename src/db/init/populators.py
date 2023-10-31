from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.user_crud import UserCrud
from db.models.user import UserTypesEnum
from db.schemas.user_schema import UserCreate
from settings import settings


async def populate_users(session: AsyncSession):
    user_crud = UserCrud(session)
    user = await user_crud.get_by_name(name=settings.FIRST_SUPERUSER_NAME)
    if not user:
        user_in = UserCreate(
            name=settings.FIRST_SUPERUSER_NAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            user_type=UserTypesEnum.ADMIN,
        )
        await user_crud.create_user(user=user_in)
