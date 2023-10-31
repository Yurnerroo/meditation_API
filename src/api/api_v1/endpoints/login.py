from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import (
    CurrentUser,
    UserCrudSession, CurrentSuperUser,
)
from auth.jwthandler import create_access_token
from db.schemas.user_schema import UserCreate, UserRead, UserReadResponse
from schemas import token as token_schema
from settings import settings

router = APIRouter()


@router.post("/register", response_model=UserReadResponse, status_code=201)
async def create_user(
    user: UserCreate,
    user_crud: UserCrudSession,
    current_user: CurrentSuperUser,
):
    """
    Create new user.
    """
    db_user = await user_crud.get_by_username_or_email(
        username=user.username, email=user.email
    )
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    result = await user_crud.create_user(user)

    # check if any error returnde from db
    if isinstance(result, dict):
        raise HTTPException(status_code=400, detail=result)

    return result


@router.post("/access-token", response_model=token_schema.Token)
async def login_access_token(
    user_crud: UserCrudSession,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_crud.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            str(user.id), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=UserRead)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
