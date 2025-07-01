"""
Breach data endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from app.core.database import get_db
from app.models.database import BreachData, ThreatLevel
from app.api.v1.endpoints.auth import verify_token

router = APIRouter()


class ThreatLevelEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BreachResponse(BaseModel):
    id: int
    source_id: int
    title: str
    content: str
    url: Optional[str]
    threat_level: Optional[str]
    categories: Optional[List[str]]
    confidence_score: Optional[float]
    keywords_matched: Optional[List[str]]
    discovered_at: str
    processed_at: Optional[str]
    is_verified: bool
    is_false_positive: bool

    class Config:
        from_attributes = True


class BreachStats(BaseModel):
    total_breaches: int
    breaches_today: int
    critical_breaches: int
    high_breaches: int
    unprocessed_breaches: int


@router.get("/", response_model=List[BreachResponse])
async def list_breaches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    threat_level: Optional[ThreatLevelEnum] = None,
    source_id: Optional[int] = None,
    is_verified: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """List breach data"""
    query = select(BreachData).order_by(desc(BreachData.discovered_at))
    
    # Apply filters
    conditions = []
    if threat_level:
        conditions.append(BreachData.threat_level == threat_level.value)
    if source_id:
        conditions.append(BreachData.source_id == source_id)
    if is_verified is not None:
        conditions.append(BreachData.is_verified == is_verified)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    breaches = result.scalars().all()
    
    return [
        BreachResponse(
            id=breach.id,
            source_id=breach.source_id,
            title=breach.title,
            content=breach.content[:500] + "..." if len(breach.content) > 500 else breach.content,
            url=breach.url,
            threat_level=breach.threat_level.value if breach.threat_level else None,
            categories=breach.categories,
            confidence_score=breach.confidence_score,
            keywords_matched=breach.keywords_matched,
            discovered_at=breach.discovered_at.isoformat(),
            processed_at=breach.processed_at.isoformat() if breach.processed_at else None,
            is_verified=breach.is_verified,
            is_false_positive=breach.is_false_positive
        )
        for breach in breaches
    ]


@router.get("/stats", response_model=BreachStats)
async def get_breach_stats(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get breach statistics"""
    from datetime import datetime, timedelta
    
    today = datetime.utcnow().date()
    
    # Total breaches
    total_result = await db.execute(select(BreachData).count())
    total_breaches = total_result.scalar() or 0
    
    # Breaches today
    today_result = await db.execute(
        select(BreachData).where(
            BreachData.discovered_at >= today
        ).count()
    )
    breaches_today = today_result.scalar() or 0
    
    # Critical breaches
    critical_result = await db.execute(
        select(BreachData).where(
            BreachData.threat_level == ThreatLevel.CRITICAL
        ).count()
    )
    critical_breaches = critical_result.scalar() or 0
    
    # High threat breaches
    high_result = await db.execute(
        select(BreachData).where(
            BreachData.threat_level == ThreatLevel.HIGH
        ).count()
    )
    high_breaches = high_result.scalar() or 0
    
    # Unprocessed breaches
    unprocessed_result = await db.execute(
        select(BreachData).where(
            BreachData.processed_at.is_(None)
        ).count()
    )
    unprocessed_breaches = unprocessed_result.scalar() or 0
    
    return BreachStats(
        total_breaches=total_breaches,
        breaches_today=breaches_today,
        critical_breaches=critical_breaches,
        high_breaches=high_breaches,
        unprocessed_breaches=unprocessed_breaches
    )


@router.get("/{breach_id}", response_model=BreachResponse)
async def get_breach(
    breach_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get a specific breach"""
    result = await db.execute(select(BreachData).where(BreachData.id == breach_id))
    breach = result.scalar_one_or_none()
    
    if not breach:
        raise HTTPException(status_code=404, detail="Breach not found")
    
    return BreachResponse(
        id=breach.id,
        source_id=breach.source_id,
        title=breach.title,
        content=breach.content,
        url=breach.url,
        threat_level=breach.threat_level.value if breach.threat_level else None,
        categories=breach.categories,
        confidence_score=breach.confidence_score,
        keywords_matched=breach.keywords_matched,
        discovered_at=breach.discovered_at.isoformat(),
        processed_at=breach.processed_at.isoformat() if breach.processed_at else None,
        is_verified=breach.is_verified,
        is_false_positive=breach.is_false_positive
    )


@router.put("/{breach_id}/verify")
async def verify_breach(
    breach_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Mark a breach as verified"""
    result = await db.execute(select(BreachData).where(BreachData.id == breach_id))
    breach = result.scalar_one_or_none()
    
    if not breach:
        raise HTTPException(status_code=404, detail="Breach not found")
    
    breach.is_verified = True
    await db.commit()
    
    return {"message": "Breach verified successfully"}


@router.put("/{breach_id}/false-positive")
async def mark_false_positive(
    breach_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Mark a breach as false positive"""
    result = await db.execute(select(BreachData).where(BreachData.id == breach_id))
    breach = result.scalar_one_or_none()
    
    if not breach:
        raise HTTPException(status_code=404, detail="Breach not found")
    
    breach.is_false_positive = True
    await db.commit()
    
    return {"message": "Breach marked as false positive"}