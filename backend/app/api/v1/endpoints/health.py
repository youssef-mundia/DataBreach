"""
Health check endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import psutil
import time

from app.core.database import DatabaseManager
from config.settings import settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    timestamp: float
    version: str
    database: Dict[str, Any]
    system: Dict[str, Any]


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check"""
    try:
        # Database health
        db_status = await DatabaseManager.health_check()
        db_stats = await DatabaseManager.get_stats()
        
        # System health
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        system_info = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": memory.percent,
            "memory_available": memory.available,
            "disk_percent": (disk.used / disk.total) * 100,
            "disk_free": disk.free
        }
        
        return HealthResponse(
            status="healthy",
            timestamp=time.time(),
            version=settings.APP_VERSION,
            database={
                "connectivity": db_status,
                "stats": db_stats
            },
            system=system_info
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@router.get("/database")
async def database_health():
    """Database-specific health check"""
    try:
        db_status = await DatabaseManager.health_check()
        db_stats = await DatabaseManager.get_stats()
        
        return {
            "status": "healthy",
            "connectivity": db_status,
            "statistics": db_stats
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database health check failed: {str(e)}")


@router.get("/system")
async def system_health():
    """System-specific health check"""
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "status": "healthy",
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": (disk.used / disk.total) * 100
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"System health check failed: {str(e)}")