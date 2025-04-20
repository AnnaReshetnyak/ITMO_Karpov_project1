from fastapi import APIRouter, Depends, HTTPException, status
from lesson_2.app.rabbitmq.producer import send_prediction_task
from lesson_2.app.database.services.crud.prediction import PredictionCRUD
from lesson_2.app.database.services.crud.balance_crud import BalanceCRUD
from lesson_2.app.models import User
from lesson_2.app.schemas import PredictionRequest, TaskResponse
from lesson_2.app.dependencies import get_current_user, get_crud
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["predictions"])

@router.post("/predict", response_model=TaskResponse)
async def create_prediction(
        request: PredictionRequest,
        user: User = Depends(get_current_user),
        prediction_crud: PredictionCRUD = Depends(get_crud(PredictionCRUD)),
        balance_crud: BalanceCRUD = Depends(get_crud(BalanceCRUD))
):
    logger.info(
        f"Starting prediction request | User: {user.id} | "
        f"Input data size: {len(str(request.input_data))}"
    )
    
    try:
        # Рассчитываем стоимость запроса
        cost = calculate_cost(request.input_data)
        logger.debug(f"Calculated cost: {cost} | User: {user.id}")

        # Получаем текущий баланс
        current_balance = await balance_crud.get_user_balance(user.id)
        logger.debug(f"Current balance: {current_balance} | User: {user.id}")

        # Проверяем достаточно ли средств
        if current_balance < cost:
            logger.warning(
                f"Insufficient balance | User: {user.id} | "
                f"Balance: {current_balance} | Required: {cost}"
            )
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
        logger.info(f"Task created | TaskID: {task.id} | User: {user.id}")

        # Списание средств
        new_balance = await balance_crud.make_transaction(
            user_id=user.id,
            amount=-cost,
            type="PREDICTION",
            description=f"Списание за задачу {task.id}"
        )
        logger.info(
            f"Balance updated | TaskID: {task.id} | "
            f"New balance: {new_balance} | User: {user.id}"
        )

        # Отправка задачи в очередь
        await send_prediction_task({
            "task_id": str(task.id),
            "input_data": request.input_data
        })
        logger.debug(f"Task sent to RabbitMQ | TaskID: {task.id}")

        logger.info(f"Prediction successful | TaskID: {task.id}")
        return TaskResponse(
            task_id=task.id,
            status=task.status,
            created_at=task.created_at
        )

    except HTTPException:
        # Уже обработанные ошибки
        raise
    except Exception as e:
        logger.error(
            f"Prediction failed | User: {user.id} | "
            f"Error: {str(e)} | Input: {request.input_data}",
            exc_info=True
        )
        if task:
            await prediction_crud.update_task_status(
                task.id,
                status="failed",
                result={"error": str(e)}
            )
            logger.warning(f"Task marked as failed | TaskID: {task.id}")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обработки задачи: {str(e)}"
        )

def calculate_cost(input_data: dict) -> float:
    """Расчет стоимости запроса"""
    cost = len(str(input_data)) * 0.001
    logger.debug(f"Cost calculation | Data length: {len(str(input_data))} | Cost: {cost}")
    return cost
