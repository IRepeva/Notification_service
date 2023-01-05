import json
import logging

import pika
import pika.exceptions
from core.settings import settings
from services.message_handler import MessageHandler
from services.publisher import RabbitPublisher
from utils.backoff import backoff

logger = logging.getLogger(__name__)


class RabbitConsumer:
    def __init__(
            self,
            publisher: RabbitPublisher,
            renderer: MessageHandler,
    ) -> None:
        self.publisher = publisher
        self.renderer = renderer

        credentials = pika.PlainCredentials(
            settings.rabbit.username,
            settings.rabbit.password.get_secret_value()
        )
        parameters = pika.ConnectionParameters(
            settings.rabbit.host, settings.rabbit.port, credentials=credentials
        )
        self.connection = pika.SelectConnection(
            parameters, on_open_callback=self.on_connected
        )
        self.start()

    def on_connected(self, connection):
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, new_channel):
        self.channel = new_channel
        self.channel.queue_declare(
            queue=settings.rabbit.consumer_queue,
            durable=True,
            exclusive=False,
            auto_delete=False,
            callback=self.on_queue_declared
        )

    def on_queue_declared(self, frame):
        self.channel.basic_consume(
            settings.rabbit.consumer_queue, self.handle_delivery
        )

    def handle_delivery(self, channel, method, properties, body):
        logger.info('New message %s %s', body, properties.headers)

        try:
            message = json.loads(body)
        except json.JSONDecodeError:
            logger.exception('JSON Decode error format: %s', body)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

        logger.info('Message decoded %s', message)

        notifications = self.renderer.process_message(message)
        for notification in notifications:
            self.publisher.publish(notification.dict(), properties.headers)

        channel.basic_ack(delivery_tag=method.delivery_tag)
        logger.info('Message was processed.')

    @backoff()
    def start(self):
        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()
            self.connection.ioloop.start()
