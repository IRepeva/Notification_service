import json
import logging

import pika
import pika.exceptions
from senders.base_sender import BaseSender
from utils.backoff import backoff

from core.settings import settings

logger = logging.getLogger(__name__)


class Worker:

    def __init__(self, sender: BaseSender, template) -> None:
        self.sender = sender
        self.template = template

        credentials = pika.PlainCredentials(
            settings.rabbit.username,
            settings.rabbit.password.get_secret_value()
        )
        parameters = pika.ConnectionParameters(
            settings.rabbit.host,
            settings.rabbit.port,
            credentials=credentials
        )
        self.connection = pika.SelectConnection(
            parameters,
            on_open_callback=self.on_connected
        )
        self.start()

    def on_connected(self, connection):
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, new_channel):
        self.channel = new_channel
        self.channel.queue_declare(
            queue=settings.rabbit.queue,
            durable=True,
            exclusive=False,
            auto_delete=False,
            callback=self.on_queue_declared
        )

    def on_queue_declared(self, frame):
        self.channel.basic_consume(settings.rabbit.queue, self.handle_delivery)

    def handle_delivery(self, channel, method, parameters, message):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.warning("RabbitMQ message can't be handled")

        to_send = self.template.parse_obj(message)
        self.sender.send(data=to_send)
        logger.warning("Message was sent")

        channel.basic_ack(delivery_tag=method.delivery_tag)

    @backoff()
    def start(self):
        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()
            self.connection.ioloop.start()
