from typing import Annotated

from fastapi import Depends

from auth.jwthandler import (
    get_current_active_superuser,
    get_current_active_user,
    get_current_user,
)
from db.crud.user_crud import UserCrud
from db.models.user import User
from dependencies import get_user_crud

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]
CurrentSuperUser = Annotated[User, Depends(get_current_active_superuser)]

UserCrudSession = Annotated[UserCrud, Depends(get_user_crud)]
