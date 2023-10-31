import logging
from typing import Any

from sqlalchemy import and_, or_, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth.users import get_password_hash, verify_password
from db.crud.base_crud import BaseCrud
from db.models.user import User, UserTypesEnum
from db.schemas.user_schema import UserCreate, UserUpdate, UserFilter, UserReadResponse
from schemas.common_schema import IOrderEnum

logger = logging.Logger(__name__)


class UserCrud(BaseCrud[User, UserCreate, UserUpdate]):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        super().__init__(model=User, db_session=db_session)

    async def get(self, id_: int) -> User | None:
        return await super().get(id_=id_)

    async def get_by_name(self, *, name: str) -> User | None:
        stmt = select(User).where(User.name == name)  # type: ignore
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all_users_ordered(
        self,
        users_filter: UserFilter,
        order_by: Any = None,
    ) -> list[UserReadResponse] | None:
        query = self._get_all_users_query(
            users_filter=users_filter,
            order_by=order_by,
        )
        db_result = (await self.db.execute(query)).fetchall()
        return [
            UserReadResponse(
                id=row[0].id,
                name=row[0].name,
                avatar=row[0].avatar,
                user_type=row[0].user_type,
            ) for row in db_result
        ] if db_result else None

    async def create_admin_user(self, user: UserCreate) -> User:
        db_user = User(
            name=user.name,
            avatar=user.avatar,
            password_hash=get_password_hash(user.password),
            user_type=UserTypesEnum.ADMIN,
        )
        self.db.add(db_user)
        await self.db.flush()
        return db_user

    async def create_user(self, user: UserCreate) -> User:
        db_user = User(
            name=user.name,
            avatar=user.avatar,
            password_hash=get_password_hash(user.password),
        )
        self.db.add(db_user)
        await self.db.flush()
        return db_user

    async def update(
        self, *, db_obj: User, obj_in: UserUpdate | dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            password_hash = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password_hash"] = password_hash

        return await super().update(db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, *, username: str, password: str) -> User | None:
        user = await self.get_by_name(name=username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def is_superuser(user: User) -> bool:
        return user.user_type == UserTypesEnum.ADMIN

    @staticmethod
    def _get_all_users_query(
            users_filter: UserFilter,
            order_by: Any,
            order: IOrderEnum | None = None,
    ) -> Select:
        query = (
            select(User)
            .where(
                and_(
                    or_(not users_filter.name, User.name == users_filter.name),
                    or_(not users_filter.user_type, User.user_type == users_filter.user_type),
                )
            )
        )

        if order == IOrderEnum.ascendent:
            query = query.order_by(order_by.asc())
        else:
            query = query.order_by(order_by.desc())  # type: ignore

        return query
