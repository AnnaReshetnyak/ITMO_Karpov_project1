from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.database import get_session
from app.schemas import BalanceResponse, TopUpRequest
from app.dependencies import get_current_user
from app.database.services.crud.balance_crud import BalanceCRUD
from app.database.services.crud.transaction_crud import  TransactionCRUD


router = APIRouter(prefix="/balance", tags=["balance"])


@router.get("/", response_model=BalanceResponse)
async def get_balance(
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    balance_crud = BalanceCRUD(session)
    balance = balance_crud.get_by_user(current_user.id)
    return {"balance": balance.amount}


@router.post("/topup", response_model=BalanceResponse)
async def topup_balance(
        topup_data: TopUpRequest,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    balance_crud = BalanceCRUD(session)
    transaction_crud = TransactionCRUD(session)

    # Обновление баланса
    new_balance = balance_crud.update_balance(
        user_id=current_user.id,
        amount=topup_data.amount
    )

    # Логирование транзакции
    transaction_crud.create({
        "user_id": current_user.id,
        "amount": topup_data.amount,
        "type": "DEPOSIT",
        "description": "Balance top up"
    })

    return {"balance": new_balance.amount}
