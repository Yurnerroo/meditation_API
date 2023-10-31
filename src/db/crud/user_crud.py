import logging
from typing import Any

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import func, BooleanClauseList
from sqlalchemy.exc import ArgumentError, DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from sqlalchemy.sql import and_, or_

from auth.users import get_password_hash, verify_password
from db.crud.base_crud import BaseCrud
from db.models.user import User
from db.schemas.user_schema import UserCreate, UserUpdate

logger = logging.Logger(__name__)


class UserCrud(BaseCrud[User, UserCreate, UserUpdate]):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        super().__init__(model=User, db_session=db_session)

    async def get(self, id_: int) -> User | None:
        return await super().get(id_=id_)

    async def get_by_name(self, *, name: str) -> User | None:
        stmt = select(User).where(User.username == name)  # type: ignore
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create_user(self, user: UserCreate) -> User | dict[str, Any]:
        try:
            db_user = User(
                username=user.username,
                password_hash=get_password_hash(user.password),
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_super_user=user.is_super_user,
                is_approved=user.is_approved,
                created_by_user_id=user.created_by_user_id,
            )
            self.db.add(db_user)
            await self.db.flush()
            return db_user
        except IntegrityError as ie:
            if "foreign key constraint" in str(ie.orig):
                return {"error": "Invalid Country ID or Language ID."}
            else:
                return {"error": "Database integrity error."}
        except ArgumentError as ae:
            # Handle invalid arguments error
            return {"error": "Invalid Argument passed."}
        except DataError as de:
            # Handle data related error like wrong type or length of a field
            return {"error": "Invalid Data passed."}
        except Exception as e:
            # General catch all for other exceptions
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

