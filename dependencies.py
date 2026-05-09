"""
Wiring de Inyección de Dependencias.
Centraliza la construcción del grafo de objetos: Repository -> Service.
Los controllers importan desde aquí; nunca instancian directamente.
"""

from fastapi import Depends

from repositories.article_repository import ArticleRepository, IArticleRepository
from services.article_service import ArticleService


def get_article_repository() -> IArticleRepository:
    return ArticleRepository()


def get_article_service(
    repository: IArticleRepository = Depends(get_article_repository),
) -> ArticleService:
    return ArticleService(repository=repository)
