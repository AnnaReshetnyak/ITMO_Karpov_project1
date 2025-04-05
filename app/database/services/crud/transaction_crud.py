from sqlmodel import Session, select
from typing import List, Optional
from app.models import Transaction

class TransactionCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, transaction_data: dict) -> Transaction:
        db_transaction = Transaction(**transaction_data)
        self.session.add(db_transaction)
        self.session.commit()
        self.session.refresh(db_transaction)
        return db_transaction

    def get(self, transaction_id: int) -> Optional[Transaction]:
        return self.session.get(Transaction, transaction_id)

    def get_all_by_user(self, user_id: int) -> List[Transaction]:
        statement = select(Transaction).where(Transaction.user_id == user_id)
        result = self.session.exec(statement)
        return result.all()
