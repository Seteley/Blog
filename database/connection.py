import os
from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.extensions

_HOST     = os.getenv("DB_HOST",     "localhost")
_PORT     = os.getenv("DB_PORT",     "5432")
_DATABASE = os.getenv("DB_NAME",     "blogdb")
_USERNAME = os.getenv("DB_USER",     "postgres")
_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


@contextmanager
def get_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    Context manager que entrega una conexión transaccional.
    Hace commit si el bloque termina sin excepciones; rollback si falla.
    """
    conn: psycopg2.extensions.connection = psycopg2.connect(
        host=_HOST,
        port=int(_PORT),
        dbname=_DATABASE,
        user=_USERNAME,
        password=_PASSWORD,
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
