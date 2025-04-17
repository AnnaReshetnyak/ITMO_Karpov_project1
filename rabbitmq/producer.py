import aio_pika
import json
from lesson_2.app.database.config import settings

async def send_prediction_task(task_data: dict):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(task_data).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=settings.RABBITMQ_QUEUE
        )
