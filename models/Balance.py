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

