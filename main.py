

class User:
    def __init__(self, user_id: int, username: str, email: str, balance: 'Balance'):
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__balance = balance

    def get_user_info(self) -> dict:
        return {
            "user_id": self.__user_id,
            "username": self.__username,
            "email": self.__email,
            "balance": self.__balance.get_amount()
        }

    def get_balance(self) -> float:
        return self.__balance.get_amount()

class MLModel:
    def __init__(self, model_id: int, model_name: str):
        self.__model_id = model_id
        self.__model_name = model_name
        self.__is_trained = False

    def train(self, data: list) -> None:
        # Логика обучения модели
        self.__is_trained = True
        print(f"Model {self.__model_name} trained successfully.")

    def predict(self, input_data: dict) -> dict:
        if not self.__is_trained:
            raise Exception("Model is not trained yet.")
        # Логика предсказания
        return {"prediction": "sample_prediction"}

    def get_model_info(self) -> dict:
        return {
            "model_id": self.__model_id,
            "model_name": self.__model_name,
            "is_trained": self.__is_trained
        }

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


class MLTask:
    def __init__(self, task_id: int, model: MLModel, input_data: dict):
        self.__task_id = task_id
        self.__model = model
        self.__input_data = input_data

    def execute_task(self) -> dict:
        return self.__model.predict(self.__input_data)

class Balance:
    def __init__(self, initial_amount: float = 0.0):
        self.__amount = initial_amount

    def add_funds(self, amount: float) -> None:
        self.__amount += amount

    def deduct_funds(self, amount: float) -> None:
        if self.__amount < amount:
            raise ValueError("Insufficient funds.")
        self.__amount -= amount

    def get_amount(self) -> float:
        return self.__amount


# Создаем баланс для пользователя
balance = Balance(100.0)

# Создаем пользователя
user = User(1, "anna_resh", "annaresh@example.com", balance)

# Создаем ML-модель
model = MLModel(1, "Sentiment Analysis Model")

# Обучаем модель
model.train(["sample data"])

# Создаем задачу для ML-модели
task = MLTask(1, model, {"text": "This is a great product!"})

# Выполняем задачу
prediction_result = task.execute_task()

# Добавляем запись в историю
history = PredictionHistory()
history.add_record(user.get_user_info()["user_id"], prediction_result)

# Получаем историю пользователя
user_history = history.get_history(1)
print(user_history)


