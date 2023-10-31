from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from starlette import status

from api.deps import (
    CurrentActiveUser,
    CurrentUser,
    UserCrudSession,
)
from db.models.user import User
from db.schemas.user_schema import (
    UserFilter,
    UserReadResponse,
    UserUpdate,
    UserUpdateMe,
)
from schemas.common_schema import IOrderEnum

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


@router.get("/paginated/")
async def read_users(
    user_crud: UserCrudSession,
    users_filter: UserFilter = Depends(),
    params: Params = Depends(),
):
    """
    Retrieve users.
    """
    result = await user_crud.get_multi_paginated_ordered(
        params=params,
        order=IOrderEnum.descendent,
        filter_exp=users_filter,
    )

    if not result:
        raise HTTPException(status_code=404)
    return result


@router.get("/search_users_paginated/")
async def search_users_paginated(
    searched_substr: str,
    user_crud: UserCrudSession,
    current_user: CurrentActiveUser,
    params: Params = Depends(),
):
    return await user_crud.search_users_paginated(
        params=params,
        searched_substr=searched_substr,
        created_by_user_id=current_user.id,
    )


@router.get("/")
async def get_all_users(
    user_crud: UserCrudSession,
):
    """
    Retrieve all users.
    """

    return await user_crud.get_all_users_ordered(order_by=User.name)


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
    user = await user_crud.update(db_obj=current_user, obj_in=user_in)
    return user


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
