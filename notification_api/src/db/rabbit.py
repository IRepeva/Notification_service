from typing import Optional
import pika

rabbitmq: Optional[pika.BlockingConnection] = None


async def get_rabbit():
    return rabbitmq
