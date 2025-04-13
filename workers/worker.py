import aio_pika
from lesson_2.app.ml.model import predict
from lesson_2.app.database.database import save_prediction
import json

async def process_task(message: aio_pika.IncomingMessage):
    async with message.process():
        task_data = json.loads(message.body.decode())

        # Валидация данных
        if not validate_input(task_data["input"]):
            return

        # Выполнение предсказания
        result = predict(task_data["input"])

        # Сохранение результата
        await save_prediction({
            "user_id": task_data["user_id"],
            "input_data": task_data["input"],
            "result": result
        })
