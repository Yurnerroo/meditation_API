import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router
from db.init.init_db import init_db
from logger import get_uvicorn_log_config, init_logger
from settings import settings

init_logger()

app = FastAPI(
    title=settings.PROJECT_NAME,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)
app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def main() -> None:
    if settings.INIT_DB_IF_NOT_INITIALIZED:
        await init_db()


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(
        "main:app",
        port=settings.APP_PORT,
        host=settings.APP_HOST,
        reload=settings.APP_RELOAD,
        log_config=get_uvicorn_log_config(),
    )
