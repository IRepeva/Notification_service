import json
import logging
from abc import ABC, abstractmethod

import pika
import pika.exceptions
from core.configuration import settings
from utils.backoff import backoff, backoff_reconnect

logger = logging.getLogger(__name__)


class BasePublisher(ABC):
    @abstractmethod
    def publish(self, message: dict, headers: dict) -> None:
        ...


class RabbitPublisher(BasePublisher):
    def __init__(self) -> None:
        credentials = pika.PlainCredentials(
            settings.rabbit.username,
            settings.rabbit.password.get_secret_value()
        )
        self.parameters = pika.ConnectionParameters(
            settings.rabbit.host, settings.rabbit.port, credentials=credentials
        )
        self.connect()

    @backoff()
    def connect(self) -> None:
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue=settings.rabbit.publisher_queue,
            durable=True,
            exclusive=False,
            auto_delete=False
        )
        self.channel.confirm_delivery()

    def reconnect(self) -> None:
        try:
            self.connection.close()
        except BaseException:
            logger.info(f'Trying to reconnect')
        self.connect()

    @backoff_reconnect()
    def publish(self, message: dict, headers: dict) -> None:
        try:
            self.channel.basic_publish(
                exchange=settings.rabbit.exchange,
                routing_key=settings.rabbit.publisher_queue,
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    headers=headers,
                    delivery_mode=pika.DeliveryMode.Transient
                ),
                mandatory=True
            )
            logger.info('Message was published')
        except pika.exceptions.UnroutableError:
            logger.error('Message was returned')
