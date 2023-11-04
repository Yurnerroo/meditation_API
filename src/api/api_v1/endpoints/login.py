from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import (
    UserCrudSession,
)
from auth.jwthandler import create_access_token
from db.schemas.user_schema import UserCreate, UserReadResponse
from schemas import token as token_schema
from settings import settings

router = APIRouter()


@router.post("/register", response_model=UserReadResponse, status_code=201)
async def create_user(
    user: UserCreate,
    user_crud: UserCrudSession,
):
    """
    Create new user.
    """
    db_user = await user_crud.get_by_name(name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    result = await user_crud.create_user(user)

    # check if any error returned from db
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
