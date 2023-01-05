import logging
import smtplib
import uuid
from email.message import EmailMessage

from models.models import EmailTemplate, Notification

from core.settings import settings
from senders.base_sender import BaseSender

logger = logging.getLogger(__name__)


class EmailSender(BaseSender):
    def _get_smtp_server_connection(self):
        server = smtplib.SMTP_SSL(settings.email.address, settings.email.port)
        server.login(settings.email.login, settings.email.password)
        return server

    def send(self, data: EmailTemplate):
        server = self._get_smtp_server_connection()
        logger.warning("SMTP connection established")

        message = EmailMessage()
        message["From"] = settings.email.login
        message["To"] = data.email
        message["Subject"] = data.subject
        message.add_alternative(data.letter, subtype='html')

        if self._was_not_sent(data.notification_id, data.user_id):
            server.send_message(message)

            notification = Notification(
                notification_id=data.notification_id,
                user_id=data.user_id,
                content_id=data.content_id,
                type='email'
            )
            self.db_service.save_notification(notification)
        server.close()

    def _was_not_sent(self, notification_id: uuid.UUID, user_id: uuid.UUID):
        if not self.db_service.get_notification_by_id(notification_id, user_id):
            return True

        logger.warning(
            f'The message {notification_id} has already been sent to {user_id}'
        )
        return False
