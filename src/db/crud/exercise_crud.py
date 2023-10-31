from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.base_crud import BaseCrud
from db.models.exercise import Exercise
from db.models.user import User, UserTypesEnum
from db.schemas.exercise_schema import (
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseReadResponse,
)
from settings import settings


class ExerciseCrud(BaseCrud[Exercise, ExerciseCreate, ExerciseUpdate]):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        super().__init__(model=Exercise, db_session=db_session)

    async def create_exercise(
        self,
        exercise_in: ExerciseCreate,
        current_user: User,
    ) -> Exercise:
        db_exercise = Exercise(
            text=exercise_in.text,
            photo=exercise_in.photo,
            time=exercise_in.time,
            owner=current_user.id,
        )
        self.db.add(db_exercise)
        await self.db.flush()

        return db_exercise

    async def get_exercises_by_owner(
        self,
        owner: int,
    ) -> list[ExerciseReadResponse]:
        query = select(self.model).where(
            self.model.owner == owner,  # type: ignore
            self.model.time > datetime.now(),  # type: ignore
        )

        result = (await self.db.execute(query)).all()
        return [
            ExerciseReadResponse(
                id=exercise[0],
                text=exercise[1],
                photo=exercise[2],
                time=exercise[3],
            )
            for exercise in result
        ]

    async def get_daily_exercise(self) -> ExerciseReadResponse:
        query = (
            select(self.model)
            .join(User, self.model.owner == User.id)  # type: ignore
            .where(
                User.name == settings.FIRST_SUPERUSER_NAME,
                User.user_type == UserTypesEnum.ADMIN,
            )
            .order_by(desc(self.model.time))
        )
        result = (await self.db.execute(query)).first()
        return ExerciseReadResponse(
            id=result[0],
            text=result[1],
            photo=result[2],
            time=result[3],
        )
