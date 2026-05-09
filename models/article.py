from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, Field


# --- Domain Model (objeto interno de negocio, sin dependencia de Pydantic) ---

@dataclass
class Article:
    id: int
    title: str
    content: str
    created_at: datetime


# --- DTOs de Entrada (Presentation -> BLL) ---

class ArticleCreateDTO(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, examples=["Mi primer artículo"])
    content: str = Field(..., min_length=10, examples=["Contenido detallado del artículo..."])


# --- DTOs de Salida (BLL -> Presentation) ---

class ArticleResponseDTO(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
