from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.user_crud import UserCrud
from db.schemas.user_schema import UserCreate
from settings import settings


async def populate_users(session: AsyncSession):
    user_crud = UserCrud(session)
    user = await user_crud.get_by_name(name=settings.FIRST_SUPERUSER_NAME)
    if not user:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER_NAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email=settings.FIRST_SUPERUSER_EMAIL,
            full_name=settings.FIRST_SUPERUSER_NAME,
            is_super_user=True,
            is_active=True,
            is_approved=True,
            country_id=1,
            language_id=1,
        )
        await user_crud.create_user(user=user_in)
