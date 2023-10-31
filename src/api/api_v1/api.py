from fastapi import APIRouter

from .endpoints import (
    healthcheck,
    login,
    users,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(healthcheck.router, tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
