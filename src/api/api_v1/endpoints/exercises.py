from fastapi import APIRouter, Depends, HTTPException

from api.deps import ExerciseCrudSession, CurrentActiveUser, CurrentSuperUser
from db.schemas.exercise_schema import (
    ExerciseCreate,
    ExerciseRead,
    ExerciseReadResponse,
    ExerciseUpdate,
)

router = APIRouter()


@router.get("/{exercise_id}", response_model=ExerciseReadResponse)
async def get_exercise_by_id(
    exercise_id: int,
    exercise_crud: ExerciseCrudSession,
):
    exercise = await exercise_crud.get(id_=exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise doesn't exist.",
        )
    return ExerciseRead.from_orm(exercise)


@router.post("/")
async def create_exercise(
    exercise: ExerciseCreate,
    exercise_crud: ExerciseCrudSession,
):
    return await exercise_crud.create(exercise=exercise)


@router.put("/{exercise_id}")
async def update_exercise(
    exercise_id: int,
    exercise_crud: ExerciseCrudSession,
    exercise_in: ExerciseUpdate = Depends(),
):
    exercise = await exercise_crud.get(id_=exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise doesn't exist.",
        )
    return await exercise_crud.update_exercise_info(
        db_exercise=exercise,
        exercise_in=exercise_in,
    )


@router.get("/all/")
async def get_exercises_for_user(
        current_user: CurrentActiveUser,
        exercise_crud: ExerciseCrudSession,
):
    return await exercise_crud.get_exercises_by_owner(owner=current_user.id)


@router.get("/daily/")
async def get_daily_exercise(exercise_crud: ExerciseCrudSession):
    return await exercise_crud.get_daily_exercise()
