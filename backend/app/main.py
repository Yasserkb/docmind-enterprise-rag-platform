from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.observability.metrics import metrics_response

app = FastAPI(title="DocMind API", version="1.0.0", description="RAG-powered document intelligence platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health/live")
def liveness() -> dict:
    return {"status": "UP", "service": "docmind-api", "environment": settings.environment}


@app.get("/health/ready")
def readiness() -> dict:
    # The local adapter is immediately usable. Production adapters should add
    # bounded dependency checks here and return 503 for required dependencies.
    return {"status": "READY", "storage": "local-adapter"}


@app.get("/health", include_in_schema=False)
def health() -> dict:
    return liveness()


@app.get("/metrics")
def metrics():
    return metrics_response()
