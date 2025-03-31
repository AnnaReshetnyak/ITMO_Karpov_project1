from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session, init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root(session: AsyncSession = Depends(get_session)):
    return {"status": "OK"}

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

class User:
    def __init__(self, user_id: int, username: str, email: str, password: str):
        self._user_id = user_id
        self._username = username
        self._email = email
        self._password_hash = self._hash_password(password)
        self.transaction_history = TransactionHistory(user_id)
        self.balance = Balance(self.transaction_history)

    @property
    def user_id(self) -> int:
        return self._user_id

    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self._password_hash)

class Admin(User):
    def view_user_history(self, user: User) -> List[Dict]:
        return user.transaction_history.get_history()


class MLModel:
    def __init__(self, model_id: int, model_name: str):
        self.__model_id = model_id
        self.__model_name = model_name
        self.__is_trained = False

class MLTask:
    def __init__(self, task_id: int, model: MLModel, input_data: dict):
        self.__task_id = task_id
        self.__model = model
        self.__input_data = input_data

    def execute_task(self) -> dict:
        return self.__model.predict(self.__input_data)

class PredictionHistory:
    def __init__(self):
        self.__history = []

    def add_record(self, user_id: int, prediction_result: dict) -> None:
        record = {
            "history_id": len(self.__history) + 1,
            "user_id": user_id,
            "prediction_result": prediction_result,
            "timestamp": "2025-21-03 12:00:00"  # Пример временной метки
        }
        self.__history.append(record)

    def get_history(self, user_id: int) -> list:
        return [record for record in self.__history if record["user_id"] == user_id]

if __name__ == "__main__":
    # Создание пользователя
    user1 = User(
        user_id=1,
        username="anna_resh",
        email="anna_resh@mail.ru",
        password="qwerty123"
    )

    # Операции с балансом
    user1.balance.add_funds(1500)
    user1.balance.deduct_funds(300)

    # Получение истории операций
    print("История операций пользователя:")
    for transaction in user1.transaction_history.get_history():
        print(f"{transaction['timestamp']} | {transaction['type']} | {transaction['amount']} ₽")

    # Администратор может просматривать историю
    admin = Admin(
        user_id=0,
        username="admin",
        email="admin@system.ru",
        password="secureAdminPassword123"
    )
    print("\nАдмин просматривает историю пользователя:")
    admin_view = admin.view_user_history(user1)
    for transaction in admin_view:
        print(f"{transaction['timestamp']} | {transaction['amount']} ₽")



