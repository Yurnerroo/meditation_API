import logging
from typing import Any

from sqlalchemy.exc import ArgumentError, DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth.users import get_password_hash, verify_password
from db.crud.base_crud import BaseCrud
from db.models.user import User, UserTypesEnum
from db.schemas.user_schema import UserCreate, UserUpdate

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

    async def create_user(self, user: UserCreate) -> User | dict[str, str]:
        try:
            db_user = User(
                name=user.name,
                avatar=user.avatar,
                user_type=user.user_type,
                password_hash=get_password_hash(user.password),
            )
            self.db.add(db_user)
            await self.db.flush()
            return db_user
        except IntegrityError:
            return {"error": "Database integrity error."}
        except ArgumentError:
            return {"error": "Invalid Argument passed."}
        except DataError:
            # Handle data related error like wrong type or length of a field
            return {"error": "Invalid data passed."}
        except Exception as e:
            return {"error": str(e)}

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

