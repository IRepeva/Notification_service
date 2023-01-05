import datetime as dt
import uuid
from abc import ABC, abstractmethod

import psycopg2.extras
from models.models import Notification
from psycopg2.extensions import connection


class BaseDBService(ABC):
    @abstractmethod
    def __init__(self, db_connection):
        self.connection = db_connection

    @abstractmethod
    def save_notification(self, notification: Notification):
        ...

    @abstractmethod
    def get_notification_by_id(
            self,
            notification_id: uuid.UUID,
            user_id: uuid.UUID
    ):
        ...


class PostgresService(BaseDBService):
    def __init__(self, pg_connection: connection, tablename: str):
        self.cursor = pg_connection.cursor()
        self.tablename = tablename
        psycopg2.extras.register_uuid()

    def _execute_query(self, query: str, values=None):
        with self.cursor() as cursor:
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            return cursor.fetchall()

    def save_notification(self, notification: Notification) -> None:
        query = f'''INSERT INTO {self.tablename} 
                    (notification_id, user_id, content_id, type, created_at)
                    VALUES (%s, %s, %s, %s, %s);
                '''
        values = (
            notification.notification_id,
            notification.user_id,
            notification.content_id,
            notification.type,
            str(dt.datetime.now()).split('.')[0]
        )
        self._execute_query(query, values)

    def get_all_notifications(self):
        return self._execute_query(f"SELECT * FROM notifications;")

    def get_notification_by_id(
            self,
            notification_id: uuid.UUID,
            user_id: uuid.UUID
    ):
        query = f"""SELECT * FROM notifications
                    WHERE notification_id='{notification_id}' 
                    AND user_id='{user_id}';
                """

        result = self._execute_query(query)
        return result[0] if result else None
