from sqlmodel import Session, select
from typing import List, Optional
from database.models import TransactionHistory

class TransactionHistoryCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_for_transaction(self, transaction_id: int) -> List[TransactionHistory]:
        statement = select(TransactionHistory).where(
            TransactionHistory.transaction_id == transaction_id
        )
        return self.session.exec(statement).all()

    def get_for_balance(self, balance_id: int) -> List[TransactionHistory]:
        statement = select(TransactionHistory).where(
            TransactionHistory.balance_id == balance_id
        )
        return self.session.exec(statement).all()
