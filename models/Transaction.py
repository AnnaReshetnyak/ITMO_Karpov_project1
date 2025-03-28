
from datetime import datetime
from typing import List, Dict, Optional
from uuid import uuid4

class TransactionType:
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"

class Transaction:
    def __init__(self, amount: float, transaction_type: str):
        self.id = str(uuid4())
        self.timestamp = datetime.now()
        self.amount = amount
        self.type = transaction_type

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "amount": self.amount,
            "type": self.type
        }

class TransactionHistory:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        sorted_transactions = sorted(
            self.transactions,
            key=lambda t: t.timestamp,
            reverse=True
        )
        return [t.to_dict() for t in sorted_transactions[:limit]]

class Balance:
    def __init__(self, transaction_history: TransactionHistory):
        self.amount: float = 0.0
        self.transaction_history = transaction_history

    def add_funds(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.amount += amount
        self.transaction_history.add_transaction(
            Transaction(amount, TransactionType.DEPOSIT)
        )

    def deduct_funds(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if self.amount < amount:
            raise ValueError("Недостаточно средств")
        self.amount -= amount
        self.transaction_history.add_transaction(
            Transaction(amount, TransactionType.WITHDRAWAL)
        )
