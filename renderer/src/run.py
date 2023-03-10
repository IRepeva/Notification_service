import logging

from core.configuration import settings
from services.consumer import RabbitConsumer
from services.data_extractor import UsersDataExtractor
from services.message_handler import EmailMessageHandler
from services.publisher import RabbitPublisher
from services.renderer import JanjaTemplateRenderer
from services.url_shortener import UrlShortener

logger = logging.getLogger()


if __name__ == '__main__':
    message_handler = EmailMessageHandler(
        UsersDataExtractor(settings.auth.url, settings.auth.authorization),
        JanjaTemplateRenderer(),
        UrlShortener(),
    )
    consumer = RabbitConsumer(
        RabbitPublisher(),
        message_handler
    )

    consumer.start()
