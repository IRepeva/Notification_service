import psycopg2
from psycopg2.extensions import connection


def create_pg_conn(db: str, host: str, port: int,
                   user: str, password: str, cursor_factory) -> connection:
    pg_connection = psycopg2.connect(
        dbname=db,
        host=host,
        port=port,
        user=user,
        password=password,
        cursor_factory=cursor_factory
    )

    return pg_connection
