from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.articles import router as articles_router

app = FastAPI(
    title="Blog API",
    description="Backend N-Tier con FastAPI, SQL puro y patrón Repository.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    return {"status": "ok"}
