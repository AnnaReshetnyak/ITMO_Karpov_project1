import aio_pika
from lesson_2.app.database.config import get_settings
import json

async def send_prediction_task(task_data: dict):
    connection = await aio_pika.connect_robust(get_settings.RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "predictions",
        aio_pika.ExchangeType.DIRECT
    )

    message = aio_pika.Message(
        body=json.dumps(task_data).encode(),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
    )

    await exchange.publish(message, routing_key="prediction_queue")
    await connection.close()
