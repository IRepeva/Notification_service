from psycopg2.extras import DictCursor

from core.settings import settings
from utils.connections import create_pg_conn
from services.database_service import PostgresService
from services.worker import Worker
from senders.email_sender import EmailSender
from models.models import EmailTemplate


if __name__ == '__main__':
    pg_settings = settings.postgres.dict()
    with create_pg_conn(**pg_settings, cursor_factory=DictCursor) as pg_conn:
        postgres_service = PostgresService(
            pg_connection=pg_conn,
            tablename='notifications'
        )
        sender = EmailSender(postgres_service)
        Worker(sender, EmailTemplate)
