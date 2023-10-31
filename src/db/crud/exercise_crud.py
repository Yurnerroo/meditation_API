from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.base_crud import BaseCrud
from db.models.exercise import Exercise
from db.schemas.exercise_schema import ExerciseCreate, ExerciseUpdate


class ExerciseCrud(BaseCrud[Exercise, ExerciseCreate, ExerciseUpdate]):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        super().__init__(model=Exercise, db_session=db_session)

    async def create(self, exercise_in: ExerciseCreate) -> Exercise:
        db_exercise = Exercise(
            text=exercise_in.text,
            photo=exercise_in.photo,
            time=exercise_in.time,
            owner=exercise_in.owner,
        )
        self.db.add(db_exercise)
        await self.db.flush()

        return db_exercise
