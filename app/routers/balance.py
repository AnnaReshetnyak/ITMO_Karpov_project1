from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
import logging
from database.database import get_session
from schemas import BalanceResponse, TopUpRequest
from dependencies import get_current_user
from database.services.crud.balance_crud import BalanceCRUD
from database.services.crud.transaction_crud import TransactionCRUD
from models import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/balance", tags=["balance"])


@router.get("/", response_model=BalanceResponse)
async def get_balance(
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    """Получение текущего баланса пользователя"""
    try:
        logger.info(
            f"Get balance request | UserID: {current_user.id} | "
            f"Email: {current_user.email}"
        )

        balance_crud = BalanceCRUD(session)
        balance = balance_crud.get_by_user(current_user.id)

        if not balance:
            logger.error(
                f"Balance not found | UserID: {current_user.id} | "
                f"Email: {current_user.email}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Balance record not found"
            )

        logger.info(
            f"Balance retrieved | UserID: {current_user.id} | "
            f"Amount: {balance.amount}"
        )
        return {"balance": balance.amount}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to get balance | UserID: {current_user.id} | "
            f"Error: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/topup", response_model=BalanceResponse)
async def topup_balance(
        topup_data: TopUpRequest,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    """Пополнение баланса пользователя"""
    try:
        logger.info(
            f"Balance topup request | UserID: {current_user.id} | "
            f"Amount: {topup_data.amount} | "
            f"Email: {current_user.email}"
        )

        balance_crud = BalanceCRUD(session)
        transaction_crud = TransactionCRUD(session)

        # Обновление баланса
        new_balance = balance_crud.update_balance(
            user_id=current_user.id,
            amount=topup_data.amount
        )

        logger.info(
            f"Balance updated | UserID: {current_user.id} | "
            f"New amount: {new_balance.amount}"
        )

        # Логирование транзакции
        transaction = transaction_crud.create({
            "user_id": current_user.id,
            "amount": topup_data.amount,
            "type": "DEPOSIT",
            "description": "Balance top up"
        })

        logger.debug(
            f"Transaction created | UserID: {current_user.id} | "
            f"TransactionID: {transaction.id} | "
            f"Type: {transaction.type}"
        )

        logger.info(
            f"Balance topup successful | UserID: {current_user.id} | "
            f"Final balance: {new_balance.amount}"
        )
        return {"balance": new_balance.amount}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Balance topup failed | UserID: {current_user.id} | "
            f"Amount: {topup_data.amount} | "
            f"Error: {str(e)}",
            exc_info=True
        )
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing balance topup"
        )
