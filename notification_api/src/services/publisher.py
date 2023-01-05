import json
import logging

import pika
import pika.exceptions

from core.settings import settings, Queue

logger = logging.getLogger(__name__)


def publish(message, connection, queue):
    try:
        channel = connection.channel()
        channel.basic_publish(
            exchange=settings.rabbit.exchange,
            routing_key=queue,
            body=json.dumps(message),
        )
        logger.info('Message was published')
    except pika.exceptions.UnroutableError:
        logger.error('Message was returned')


def get_queue(queue_sing):
    return Queue.instant.name if queue_sing else Queue.not_instant.name
