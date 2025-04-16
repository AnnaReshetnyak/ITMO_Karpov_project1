from fastapi import APIRouter, Depends, HTTPException, status
from lesson_2.app.rabbitmq.producer import send_prediction_task
from lesson_2.app.database.services.crud.prediction import PredictionCRUD
from lesson_2.app.database.services.crud.balance_crud import BalanceCRUD
from lesson_2.app.models import User
from lesson_2.app.schemas import PredictionRequest, TaskResponse
from lesson_2.app.dependencies import get_current_user, get_crud

router = APIRouter()


@router.post("/predict", response_model=TaskResponse)
async def create_prediction(
        request: PredictionRequest,
        user: User = Depends(get_current_user),
        prediction_crud: PredictionCRUD = Depends(get_crud(PredictionCRUD)),
        balance_crud: BalanceCRUD = Depends(get_crud(BalanceCRUD))
):
    # Рассчитываем стоимость запроса
    cost = calculate_cost(request.input_data)

    # Получаем текущий баланс
    current_balance = await balance_crud.get_user_balance(user.id)

    # Проверяем достаточно ли средств
    if current_balance < cost:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Недостаточно средств на балансе"
        )

    # Создаем запись задачи
    task = await prediction_crud.create_task(
        user_id=user.id,
        input_data=request.input_data,
        cost=cost
    )

    try:
        # Списание средств
        await balance_crud.make_transaction(
            user_id=user.id,
            amount=-cost,
            type="PREDICTION",
            description=f"Списание за задачу {task.id}"
        )

        # Отправка задачи в очередь
        await send_prediction_task({
            "task_id": str(task.id),
            "input_data": request.input_data
        })

    except Exception as e:
        # Откатываем транзакцию при ошибке
        await prediction_crud.update_task_status(
            task.id,
            status="failed",
            result={"error": str(e)}
        )
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обработки задачи: {str(e)}"
        )

    return TaskResponse(
        task_id=task.id,
        status=task.status,
        created_at=task.created_at
    )


def calculate_cost(input_data: dict) -> float:
    """Расчет стоимости запроса"""
    return len(str(input_data)) * 0.001  # Пример расчета
