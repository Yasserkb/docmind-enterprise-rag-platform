from fastapi import APIRouter

from app.api.agent import router as agent_router
from app.api.collections import router as collections_router
from app.api.demo import router as demo_router
from app.api.documents import router as documents_router
from app.api.evaluation import router as evaluation_router
from app.api.metrics import router as metrics_router
from app.api.query import router as query_router

api_router = APIRouter()
api_router.include_router(collections_router)
api_router.include_router(documents_router)
api_router.include_router(query_router)
api_router.include_router(agent_router)
api_router.include_router(evaluation_router)
api_router.include_router(metrics_router)
api_router.include_router(demo_router)
