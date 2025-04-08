from fastapi import APIRouter

home_router = APIRouter()

@home_router.get('/', tags=['Home'])
async def index() -> str:
    return "Wellcome to service!"
