import bcrypt
from datetime import datetime
from typing import List, Dict, Optional

class Balance:
    def __init__(self, user_id: int, initial_amount: float = 0.0):
        self.__user_id = user_id
        self.__amount = initial_amount

    def add_funds(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.__amount += amount

    def deduct_funds(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if self.__amount < amount:
            raise ValueError("Недостаточно средств")
        self.__amount -= amount

    @property
    def amount(self) -> float:
        return self.__amount

class User:
    def __init__(self, user_id: int, username: str, email: str, password: str):
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__password_hash = self._hash_password(password)
        self.__balance = Balance(user_id=user_id)  # Объект Balance
        self.__transactions: List[Transaction] = []

    @property
    def balance(self) -> Balance:
        return self.__balance

    @property
    def user_id(self) -> int:
        return self.__user_id

    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.__password_hash)

class Admin(User):
    def __init__(self, user_id: int, username: str, email: str, password: str):
        super().__init__(user_id, username, email, password)
        self.__is_admin = True

    def view_all_transactions(self, users: List[User]) -> None:
        for user in users:
            print(f"История пользователя {user.user_id}: {user.transactions}")

class Transaction:
    def __init__(self, amount: float, transaction_type: str):
        self.__timestamp = datetime.now()
        self.__amount = amount
        self.__type = transaction_type

    @property
    def details(self) -> Dict:
        return {
            "type": self.__type,
            "amount": self.__amount,
            "timestamp": self.__timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }

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

# Пример использования
if __name__ == "__main__":
    # Создаем пользователя
    regular_user = User(
        user_id=1,
        username="anna_resh",
        email="anna_resh@example.com",
        password="securepass"
    )

    # Пополняем баланс через объект Balance
    regular_user.balance.add_funds(150.0)
    print(f"Баланс: {regular_user.balance.amount}")  # 150.0

    # Создаем администратора
    admin = Admin(
        user_id=2,
        username="admin",
        email="admin@example.com",
        password="adminpass"
    )

