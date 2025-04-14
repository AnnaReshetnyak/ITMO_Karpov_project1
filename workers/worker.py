import json
import aio_pika
from sqlmodel.ext.asyncio.session import AsyncSession
from lesson_2.app.ml.model import model
from lesson_2.app.database.services.crud.prediction import PredictionCRUD
from lesson_2.app.database.config import settings


async def process_task(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            task_data = json.loads(message.body.decode())

            async with AsyncSession() as session:
                crud = PredictionCRUD(session)

                # Обновляем статус задачи
                task = await crud.update_task_status(
                    task_data["task_id"],
                    "processing"
                )

                # Выполняем предсказание
                result = model.predict(task.input_data)

                # Сохраняем результат
                await crud.update_task_status(
                    task.id,
                    "completed",
                    result=result
                )

        except Exception as e:
            await crud.update_task_status(
                task_data["task_id"],
                "failed",
                {"error": str(e)}
            )


async def start_worker():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("prediction_queue", durable=True)

    await queue.bind(exchange="predictions", routing_key="prediction_queue")
    await queue.consume(process_task)
