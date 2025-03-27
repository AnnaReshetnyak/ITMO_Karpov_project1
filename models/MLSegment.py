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
        return [record for record in self.__history if record["user_id"] == user_i
