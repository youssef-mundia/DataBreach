"""
Monitoring sources endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from enum import Enum

from app.core.database import get_db
from app.models.database import MonitoringSource, SourceType, SourceStatus
from app.api.v1.endpoints.auth import verify_token

router = APIRouter()


class SourceTypeEnum(str, Enum):
    DEEP_WEB = "deep_web"
    TELEGRAM = "telegram"
    FORUM = "forum"
    MARKETPLACE = "marketplace"


class SourceStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    AUTHENTICATION_FAILED = "auth_failed"


class SourceCreate(BaseModel):
    name: str
    url: HttpUrl
    source_type: SourceTypeEnum
    keywords: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    status: Optional[SourceStatusEnum] = None
    keywords: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None


class SourceResponse(BaseModel):
    id: int
    name: str
    url: str
    source_type: str
    status: str
    keywords: Optional[List[str]]
    last_checked: Optional[str]
    last_success: Optional[str]
    error_count: int
    error_message: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[SourceResponse])
async def list_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    source_type: Optional[SourceTypeEnum] = None,
    status: Optional[SourceStatusEnum] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """List monitoring sources"""
    query = select(MonitoringSource)
    
    # Apply filters
    conditions = []
    if source_type:
        conditions.append(MonitoringSource.source_type == source_type.value)
    if status:
        conditions.append(MonitoringSource.status == status.value)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    sources = result.scalars().all()
    
    return [
        SourceResponse(
            id=source.id,
            name=source.name,
            url=str(source.url),
            source_type=source.source_type.value,
            status=source.status.value,
            keywords=source.keywords,
            last_checked=source.last_checked.isoformat() if source.last_checked else None,
            last_success=source.last_success.isoformat() if source.last_success else None,
            error_count=source.error_count,
            error_message=source.error_message,
            created_at=source.created_at.isoformat()
        )
        for source in sources
    ]


@router.post("/", response_model=SourceResponse)
async def create_source(
    source_data: SourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create a new monitoring source"""
    source = MonitoringSource(
        name=source_data.name,
        url=str(source_data.url),
        source_type=SourceType(source_data.source_type.value),
        keywords=source_data.keywords,
        config=source_data.config or {}
    )
    
    db.add(source)
    await db.commit()
    await db.refresh(source)
    
    return SourceResponse(
        id=source.id,
        name=source.name,
        url=str(source.url),
        source_type=source.source_type.value,
        status=source.status.value,
        keywords=source.keywords,
        last_checked=source.last_checked.isoformat() if source.last_checked else None,
        last_success=source.last_success.isoformat() if source.last_success else None,
        error_count=source.error_count,
        error_message=source.error_message,
        created_at=source.created_at.isoformat()
    )


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get a specific monitoring source"""
    result = await db.execute(select(MonitoringSource).where(MonitoringSource.id == source_id))
    source = result.scalar_one_or_none()
    
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    return SourceResponse(
        id=source.id,
        name=source.name,
        url=str(source.url),
        source_type=source.source_type.value,
        status=source.status.value,
        keywords=source.keywords,
        last_checked=source.last_checked.isoformat() if source.last_checked else None,
        last_success=source.last_success.isoformat() if source.last_success else None,
        error_count=source.error_count,
        error_message=source.error_message,
        created_at=source.created_at.isoformat()
    )


@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: int,
    source_data: SourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Update a monitoring source"""
    result = await db.execute(select(MonitoringSource).where(MonitoringSource.id == source_id))
    source = result.scalar_one_or_none()
    
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    # Update fields
    if source_data.name is not None:
        source.name = source_data.name
    if source_data.url is not None:
        source.url = str(source_data.url)
    if source_data.status is not None:
        source.status = SourceStatus(source_data.status.value)
    if source_data.keywords is not None:
        source.keywords = source_data.keywords
    if source_data.config is not None:
        source.config = source_data.config
    
    await db.commit()
    await db.refresh(source)
    
    return SourceResponse(
        id=source.id,
        name=source.name,
        url=str(source.url),
        source_type=source.source_type.value,
        status=source.status.value,
        keywords=source.keywords,
        last_checked=source.last_checked.isoformat() if source.last_checked else None,
        last_success=source.last_success.isoformat() if source.last_success else None,
        error_count=source.error_count,
        error_message=source.error_message,
        created_at=source.created_at.isoformat()
    )


@router.delete("/{source_id}")
async def delete_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Delete a monitoring source"""
    result = await db.execute(select(MonitoringSource).where(MonitoringSource.id == source_id))
    source = result.scalar_one_or_none()
    
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    await db.delete(source)
    await db.commit()
    
    return {"message": "Source deleted successfully"}