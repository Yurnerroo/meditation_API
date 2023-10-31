from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status

from api.deps import (
    CurrentUser,
    UserCrudSession,
    CurrentSuperUser,
)
from db.models.user import User
from db.schemas.user_schema import (
    UserFilter,
    UserReadResponse,
    UserUpdate,
    UserUpdateMe,
)

router = APIRouter()
FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions."
)


@router.get("/{user_id}")
async def read_user(
    user_id: int,
    user_crud: UserCrudSession,
):
    """
    Get user by id.
    """

    user = await user_crud.get(id_=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.get("/admin/", response_model=list[UserReadResponse] | None)
async def get_all_users(
    user_crud: UserCrudSession,
    _current_super_user: CurrentSuperUser,
    users_filter: UserFilter = Depends(),
) -> list[UserReadResponse] | None:
    """
    Retrieve all users.
    """
    return await user_crud.get_all_users_ordered(
        users_filter=users_filter,
        order_by=User.name,
    )


@router.get("/me/")
async def read_user_me(
    user_crud: UserCrudSession,
    current_user: CurrentUser,
):
    """
    Get current user.
    """
    return await user_crud.get_detailed(id_=current_user.id)


@router.put("/me/", response_model=UserReadResponse)
async def update_user_me(
    *,
    user_in_me: UserUpdateMe,
    user_crud: UserCrudSession,
    current_user: CurrentUser,
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if user_in_me.password is not None:
        user_in.password = user_in_me.password
    return await user_crud.update(db_obj=current_user, obj_in=user_in)


@router.put("/{user_id}", response_model=UserReadResponse)
async def update_user(
    *,
    user_id: int,
    user_in: UserUpdate,
    user_crud: UserCrudSession,
) -> Any:
    """
    Update a user.
    """
    user = await user_crud.get(id_=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await user_crud.update(db_obj=user, obj_in=user_in)
    return user
