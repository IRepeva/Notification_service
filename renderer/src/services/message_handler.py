import logging
from abc import ABC, abstractmethod
from typing import Generator

from core.configuration import settings
from models.schemas import EmailNotification, Notification
from pydantic import ValidationError
from services.data_extractor import UsersDataExtractor
from services.renderer import TemplateRenderer
from services.url_shortener import UrlShortener

logger = logging.getLogger()


class MessageHandler(ABC):
    @abstractmethod
    def process_message(self, message: dict) -> Generator[Notification, None, None]:
        ...


class EmailMessageHandler(MessageHandler):
    def __init__(
            self,
            users_data_extractor: UsersDataExtractor,
            template_render: TemplateRenderer,
            url_shortener: UrlShortener
    ) -> None:
        self.users_data_extractor = users_data_extractor
        self.renderer = template_render
        self.url_shortener = url_shortener

    def process_message(self, message: dict) -> Generator[Notification, None, None]:
        try:
            users = message.get('users')
            template = message.pop('template')
        except KeyError:
            logger.exception("Validation error: no users or template")
            return None

        redirect_url = message.get('redirect_url', None)
        if redirect_url:
            message['redirect_url'] = self.url_shortener.get_short_url(redirect_url)

        batch_size = settings.batch_size
        batch_count = (
            len(users) // batch_size
            if len(users) / batch_size == len(users) // batch_size
            else (len(users) // batch_size) + 1
        )
        for batch in range(batch_count):
            batch_start = batch * batch_size
            batch_end = (
                (batch + 1) * batch_size if (batch + 1) * batch_size < len(users)
                else len(users) + 1
            )
            batch_users = users[batch_start:batch_end]

            users_info = self.users_data_extractor.get_info(batch_users)
            if not users_info:
                logger.error(f'Users info not found for users: {batch_users}')
                continue

            for user_info in users_info:
                render_data = {**message, **user_info}
                letter = self.renderer.template_render(template, render_data)
                try:
                    notification = EmailNotification(
                        letter=letter,
                        **render_data
                    )
                except ValidationError:
                    logger.exception(
                        'Validation error while creating notification'
                    )
                    return
                yield notification
