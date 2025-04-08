from fastapi import APIRouter
from app.schemas import MLTaskCreate
from typing import List


ml_task_router = APIRouter(tags=["ml_tasks"])

requests = []

@ml_task_router.post("/ml_tasks", response_model=List[MLTaskCreate])
async def retrieve_all_ml_tasks() -> List[MLTaskCreate]:
    return {"message": "You request created successfully", "request": MLTaskCreate.Optional[str]}
