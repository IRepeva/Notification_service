import logging
from abc import ABC, abstractmethod
from typing import Generator

from models.schemas import EmailNotification, Notification
from pydantic import ValidationError
from services.extractor import UserDataExtractor
from services.renderer import TemplateRender
from services.url_shortener import UrlShortener

logger = logging.getLogger()


class MessageHandler(ABC):
    @abstractmethod
    def process_message(self, message: dict) -> Generator[Notification, None, None]:
        ...


class EmailMessageHandler(MessageHandler):
    def __init__(
            self,
            user_info: UserDataExtractor,
            template_render: TemplateRender,
            url_shortener: UrlShortener
    ) -> None:
        self.user_info = user_info
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

        for user in users:
            user_info = self.user_info.get_info(user)
            if not user_info:
                logger.error("User info not found for %s", user)
                continue

            render_data = {**message, **user_info}
            letter = self.renderer.template_render(template, render_data)
            try:
                notification = EmailNotification(letter=letter, **render_data)
            except ValidationError:
                logger.exception('Validation error while creating notification')
                return
            yield notification
