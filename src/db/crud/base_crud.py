from datetime import datetime as dt
from typing import Any, Generic, Sequence, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import Select

from db.models.base import Base
from db.models.user import User
from schemas.common_schema import IOrderEnum

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCrud(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db_session

    async def get(self, id_: Any) -> ModelType | None:
        query = select(self.model).where(self.model.id == id_)  # type: ignore
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: Select[tuple[ModelType]] | None = None,
    ) -> Sequence[ModelType]:
        if query is None:
            query = select(self.model).offset(skip).limit(limit)
        return (await self.db.execute(query)).scalars().all()

    async def get_all_ordered(
        self,
        order_by: Any | None = None,
        order: IOrderEnum | None = IOrderEnum.ascendent,
    ) -> Sequence[ModelType]:
        columns = self.model.__table__.columns  # type: ignore

        if order_by is None or order_by.name not in columns:
            order_by = self.model.id  # type: ignore

        if order == IOrderEnum.ascendent:
            query = select(self.model).order_by(order_by.asc())  # type: ignore
        else:
            query = select(self.model).order_by(order_by.desc())  # type: ignore
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_multi_paginated(
        self,
        *,
        params: Params | None = Params(),
        query: Select | None = None,
    ) -> Page[ModelType] | None:
        if query is None:
            query = select(self.model)  # type: ignore
        return await paginate(self.db, query, params)  # type: ignore

    async def get_multi_paginated_ordered(
        self,
        *,
        params: Params | None = Params(),
        order_by: Any | None = None,
        order: IOrderEnum | None = IOrderEnum.ascendent,
    ) -> Page[ModelType] | None:
        columns = self.model.__table__.columns  # type: ignore

        if order_by is None or order_by.name not in columns:
            order_by = self.model.id  # type: ignore

        if order == IOrderEnum.ascendent:
            query = select(self.model).order_by(order_by.asc())  # type: ignore
        else:
            query = select(self.model).order_by(order_by.desc())  # type: ignore

        return await paginate(self.db, query, params)

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        format_datetime(obj_in_data=obj_in_data)
        db_obj = self.model(**obj_in_data)  # type: ignore
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def update(
        self, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def delete(self, *, id_: Any) -> ModelType | None:
        obj = await self.get(id_)
        if not obj:
            return None

        await self.db.delete(obj)
        await self.db.flush()
        return obj


def format_datetime(obj_in_data: dict) -> dict:
    if "created_at" in obj_in_data.keys():
        obj_in_data["created_at"] = dt.strptime(
            obj_in_data["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
        )
    return obj_in_data
