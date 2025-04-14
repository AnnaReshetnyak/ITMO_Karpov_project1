from fastapi import APIRouter, Depends, HTTPException
from lesson_2.app.rabbitmq.producer import send_prediction_task
from lesson_2.app.database.services.crud.prediction import PredictionCRUD
from lesson_2.app.models import User
from lesson_2.app.schemas import PredictionRequest, TaskResponse
from lesson_2.app.dependencies import get_current_user, get_crud

router = APIRouter()


@router.post("/predict", response_model=TaskResponse)
async def create_prediction(
        request: PredictionRequest,
        user: User = Depends(get_current_user),
        crud: PredictionCRUD = Depends(get_crud)
):
    try:
        # Создаем запись задачи
        task = await crud.create_task(str(user.id), request.input_data)

        # Отправляем задачу в очередь
        await send_prediction_task({
            "task_id": str(task.id),
            "input_data": request.input_data
        })

        return TaskResponse(
            task_id=task.id,
            status=task.status,
            created_at=task.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(
        task_id: str,
        user: User = Depends(get_current_user),
        crud: PredictionCRUD = Depends(get_crud)
):
    task = await crud.get_task(task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        task_id=task.id,
        status=task.status,
        result=task.result,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
