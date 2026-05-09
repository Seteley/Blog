from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

import psycopg2.extensions

from database.connection import get_connection
from models.article import Article


# --- Interfaz (Principio de Inversión de Dependencias) ---

class IArticleRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Article]:
        ...

    @abstractmethod
    def get_by_id(self, article_id: int) -> Optional[Article]:
        ...

    @abstractmethod
    def create(self, title: str, content: str) -> Article:
        ...


# --- Implementación concreta con SQL puro (estilo ADO.NET) ---

class ArticleRepository(IArticleRepository):
    """
    Accede a PostgreSQL mediante psycopg2 con SQL puro.
    El mapeo cursor-row -> dominio se realiza manualmente (_map_row).
    No depende de ningún ORM.
    """

    def get_all(self) -> List[Article]:
        sql = """
            SELECT id, title, content, created_at
            FROM   articles
            ORDER  BY created_at DESC
        """
        with get_connection() as conn:
            cursor: psycopg2.extensions.cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [self._map_row(row) for row in rows]

    def get_by_id(self, article_id: int) -> Optional[Article]:
        sql = """
            SELECT id, title, content, created_at
            FROM   articles
            WHERE  id = %s
        """
        with get_connection() as conn:
            cursor: psycopg2.extensions.cursor = conn.cursor()
            cursor.execute(sql, (article_id,))
            row = cursor.fetchone()
            return self._map_row(row) if row else None

    def create(self, title: str, content: str) -> Article:
        # RETURNING devuelve la fila recién insertada (equivalente a OUTPUT INSERTED.* en SQL Server)
        sql = """
            INSERT INTO articles (title, content, created_at)
            VALUES (%s, %s, NOW())
            RETURNING id, title, content, created_at
        """
        with get_connection() as conn:
            cursor: psycopg2.extensions.cursor = conn.cursor()
            cursor.execute(sql, (title, content))
            row = cursor.fetchone()
            return self._map_row(row)

    # ------------------------------------------------------------------ #
    # Mapeo manual tuple -> objeto de dominio
    # ------------------------------------------------------------------ #

    @staticmethod
    def _map_row(row: tuple) -> Article:
        return Article(
            id=int(row[0]),
            title=str(row[1]),
            content=str(row[2]),
            created_at=row[3] if isinstance(row[3], datetime) else datetime.fromisoformat(str(row[3])),
        )
