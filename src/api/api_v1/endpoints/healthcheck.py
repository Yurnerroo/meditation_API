from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200)
def healthcheck():
    return {"status": "ok"}
