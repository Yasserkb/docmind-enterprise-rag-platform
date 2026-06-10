from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.observability.metrics import metrics_response

app = FastAPI(title="DocMind API", version="1.0.0", description="RAG-powered document intelligence platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict:
    return {"status": "UP", "service": "docmind-api", "environment": settings.environment}


@app.get("/metrics")
def metrics():
    return metrics_response()
