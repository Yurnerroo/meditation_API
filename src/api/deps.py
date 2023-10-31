from typing import Annotated

from fastapi import Depends

from auth.jwthandler import (
    get_current_active_superuser,
    get_current_active_user,
    get_current_user,
)
from db.crud.exercise_crud import ExerciseCrud
from db.crud.post_crud import PostCrud
from db.crud.user_crud import UserCrud
from db.models.user import User
from dependencies import get_user_crud, get_exercise_crud, get_post_crud

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]
CurrentSuperUser = Annotated[User, Depends(get_current_active_superuser)]

UserCrudSession = Annotated[UserCrud, Depends(get_user_crud)]
ExerciseCrudSession = Annotated[ExerciseCrud, Depends(get_exercise_crud)]
PostCrudSession = Annotated[PostCrud, Depends(get_post_crud)]
