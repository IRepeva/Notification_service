import json
import logging

import aio_pika

logger = logging.getLogger(__name__)


async def publish(message, connection, queue):
    async with connection:
        try:
            channel = await connection.channel()

            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(message).encode()),
                routing_key=queue,
            )
            logger.info(f'Message {message} was published to queue {queue}')
        except aio_pika.exceptions.PublishError:
            logger.error('Message was returned')


def get_queue(queue_sing):
    return 'render'
