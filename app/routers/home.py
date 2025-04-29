from fastapi import APIRouter

router = APIRouter()

@router.get('/', tags=['Home'])
async def index() -> str:
    return "Wellcome to service!"
