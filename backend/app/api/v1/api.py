"""
API router for v1 endpoints
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, sources, breaches, alerts, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(sources.router, prefix="/sources", tags=["monitoring sources"])
api_router.include_router(breaches.router, prefix="/breaches", tags=["breach data"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(health.router, prefix="/health", tags=["system health"])