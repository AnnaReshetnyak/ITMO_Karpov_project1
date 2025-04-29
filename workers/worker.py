import json
import logging
from datetime import datetime
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from sqlmodel.ext.asyncio.session import AsyncSession

import lesson_2.app.main
from lesson_2.app.config import settings
from lesson_2.app.database.services.crud.prediction import PredictionCRUD
from lesson_2.app.database.database import get_session
from lesson_2.app.schemas import TaskStatus
from lesson_2.ml.model import model
from lesson_2.ml.validation import validate_prediction_input
from lesson_2.app.config import get_rabbitmq_settings

logger = logging.getLogger(__name__)

settings = get_rabbitmq_settings()
RABBITMQ_URL = settings.AMQP_URL


async def process_message(
        message: AbstractIncomingMessage,
        session: AsyncSession
) -> None:
    """Обработка одного сообщения из очереди"""
    async with message.process():
        try:
            crud = PredictionCRUD(session)
            message_data = json.loads(message.body.decode())

            task_id = message_data["task_id"]
            input_data = message_data["input_data"]

            logger.info(f"Processing task {task_id}")

            # Получаем задачу из БД
            task = await crud.get_task(task_id)
            if not task:
                logger.error(f"Task {task_id} not found")
                return

            # Обновляем статус на PROCESSING
            task = await crud.update_task_status(
                task_id=task_id,
                status=TaskStatus.PROCESSING
            )

            # Валидация входных данных
            validated_data = validate_prediction_input(input_data)

            # Выполнение предсказания
            start_time = datetime.utcnow()
            prediction = model.predict(validated_data.dict())
            processing_time = (datetime.utcnow() - start_time).total_seconds()

            # Сохраняем результат
            result = {
                "prediction": prediction,
                "model_version": model.version,
                "processing_time": processing_time
            }

            # Обновляем статус на COMPLETED
            await crud.update_task_status(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                result=result
            )

            logger.info(f"Task {task_id} completed successfully")

        except Exception as e:
            logger.error(f"Error processing task {task_id}: {str(e)}", exc_info=True)
            error_result = {"error": str(e)}

            # Обновляем статус на FAILED
            if task:
                await crud.update_task_status(
                    task_id=task_id,
                    status=TaskStatus.FAILED,
                    result=error_result
                )


async def start_worker() -> None:
    """Запуск воркера для обработки задач"""
    connection = await aio_pika.connect_robust(lesson_2.app.main.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)  # Ограничение параллельных задач

        queue = await channel.declare_queue(
            name=settings.RABBITMQ_QUEUE,
            durable=True,
            arguments={
                "x-message-ttl": 86400000  # 24 часа в ms
            }
        )

        async with get_session() as session:
            logger.info("Worker started. Waiting for messages...")
            async for message in queue:
                await process_message(message, session)


if __name__ == "__main__":
    import asyncio
    from lesson_2.app.config import configure_logging

    configure_logging()
    asyncio.run(start_worker())
