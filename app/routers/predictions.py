from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.models import User
from app.database.database import get_session
from app.models.MLSegment import MLTask, PredictionHistory
from app.dependencies import get_current_user
from app.database.services.crud import PredictionHistoryCRUD, BalanceCRUD

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("/", response_model=PredictionHistory)
async def create_prediction(
        request: MLTask,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    # Проверка баланса
    balance_crud = BalanceCRUD(session)
    balance = balance_crud.get_by_user(current_user.id)

    # Расчет стоимости
    prediction_cost = calculate_prediction_cost(request)

    if balance.amount < prediction_cost:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient funds"
        )

    # Создание предсказания
    prediction_crud = PredictionHistoryCRUD(session)
    prediction_data = {
        "user_id": current_user.id,
        "request_data": request.dict(),
        "cost": prediction_cost
    }

    # Обновление баланса
    balance_crud.update_balance(
        current_user.id,
        balance.amount - prediction_cost
    )

    return prediction_crud.create(prediction_data)

@router.get("/history", response_model=list[PredictionHistory])
async def get_prediction_history(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    prediction_crud = PredictionHistoryCRUD(session)
    return prediction_crud.get_by_user(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
