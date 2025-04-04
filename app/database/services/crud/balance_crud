from sqlmodel import Session, select
from typing import Optional, List
from app.models.Transaction import Balance

class BalanceCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get(self, balance_id: int) -> Optional[Balance]:
        return self.session.get(Balance, balance_id)

    def get_by_user(self, user_id: int) -> Optional[Balance]:
        statement = select(Balance).where(Balance.user_id == user_id)
        return self.session.exec(statement).first()

    def update(self, balance_id: int, amount: float) -> Optional[Balance]:
        db_balance = self.get(balance_id)
        if not db_balance:
            return None
        db_balance.amount = amount
        self.session.add(db_balance)
        self.session.commit()
        self.session.refresh(db_balance)
        return db_balance
