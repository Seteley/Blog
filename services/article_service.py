from typing import List

from models.article import Article
from repositories.article_repository import IArticleRepository


class ArticleService:
    """
    Capa de Lógica de Negocio (BLL).
    Orquesta validaciones y reglas antes de delegar al repositorio.
    No conoce pyodbc ni ningún detalle de persistencia.
    """

    def __init__(self, repository: IArticleRepository) -> None:
        self._repository = repository

    # ------------------------------------------------------------------ #
    # Casos de uso públicos
    # ------------------------------------------------------------------ #

    def get_all_articles(self) -> List[Article]:
        return self._repository.get_all()

    def create_article(self, title: str, content: str) -> Article:
        self._validate_title(title)
        self._validate_content(content)

        sanitized_title   = title.strip()
        sanitized_content = content.strip()

        return self._repository.create(sanitized_title, sanitized_content)

    # ------------------------------------------------------------------ #
    # Reglas de negocio privadas
    # ------------------------------------------------------------------ #

    @staticmethod
    def _validate_title(title: str) -> None:
        stripped = title.strip()
        if len(stripped) < 3:
            raise ValueError("El título debe tener al menos 3 caracteres.")
        if len(stripped) > 200:
            raise ValueError("El título no puede superar los 200 caracteres.")

    @staticmethod
    def _validate_content(content: str) -> None:
        if len(content.strip()) < 10:
            raise ValueError("El contenido debe tener al menos 10 caracteres.")
