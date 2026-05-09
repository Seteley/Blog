import os
from typing import Generator

import psycopg2
import psycopg2.extensions

# Render inyecta DATABASE_URL automáticamente para el managed PostgreSQL.
# En local usamos variables individuales como fallback.
_DATABASE_URL = os.getenv("DATABASE_URL")
_HOST         = os.getenv("DB_HOST",     "localhost")
_PORT         = os.getenv("DB_PORT",     "5432")
_DATABASE     = os.getenv("DB_NAME",     "blogdb")
_USER         = os.getenv("DB_USER",     "postgres")
_PASSWORD     = os.getenv("DB_PASSWORD", "postgres")


def get_db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    Generador para FastAPI Depends.
    Hace commit al salir sin errores; rollback si falla.
    """
    if _DATABASE_URL:
        conn = psycopg2.connect(_DATABASE_URL)
    else:
        conn = psycopg2.connect(
            host=_HOST,
            port=int(_PORT),
            dbname=_DATABASE,
            user=_USER,
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
