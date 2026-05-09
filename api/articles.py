from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_article_service
from models.article import Article, ArticleCreateDTO, ArticleResponseDTO
from services.article_service import ArticleService

router = APIRouter(prefix="/articles", tags=["Articles"])


# ------------------------------------------------------------------ #
# Helpers de mapeo: Dominio -> DTO de salida
# ------------------------------------------------------------------ #

def _to_response(article: Article) -> ArticleResponseDTO:
    return ArticleResponseDTO(
        id=article.id,
        title=article.title,
        content=article.content,
        created_at=article.created_at,
    )


# ------------------------------------------------------------------ #
# Endpoints
# ------------------------------------------------------------------ #

@router.get(
    "/",
    response_model=List[ArticleResponseDTO],
    summary="Listar todos los artículos",
)
def list_articles(
    service: ArticleService = Depends(get_article_service),
) -> List[ArticleResponseDTO]:
    articles = service.get_all_articles()
    return [_to_response(a) for a in articles]


@router.post(
    "/",
    response_model=ArticleResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo artículo",
)
def create_article(
    dto: ArticleCreateDTO,
    service: ArticleService = Depends(get_article_service),
) -> ArticleResponseDTO:
    try:
        article = service.create_article(title=dto.title, content=dto.content)
        return _to_response(article)
    except ValueError as exc:
        # Las violaciones de reglas de negocio se traducen a 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
