"""
Alerts endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from app.core.database import get_db
from app.models.database import Alert, ThreatLevel
from app.api.v1.endpoints.auth import verify_token

router = APIRouter()


class ThreatLevelEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"


class AlertResponse(BaseModel):
    id: int
    breach_data_id: int
    title: str
    message: str
    threat_level: str
    is_sent: bool
    sent_at: Optional[str]
    sent_channels: Optional[List[str]]
    created_at: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[AlertResponse])
async def list_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    threat_level: Optional[ThreatLevelEnum] = None,
    is_sent: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """List alerts"""
    query = select(Alert).order_by(desc(Alert.created_at))
    
    # Apply filters
    conditions = []
    if threat_level:
        conditions.append(Alert.threat_level == threat_level.value)
    if is_sent is not None:
        conditions.append(Alert.is_sent == is_sent)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    alerts = result.scalars().all()
    
    return [
        AlertResponse(
            id=alert.id,
            breach_data_id=alert.breach_data_id,
            title=alert.title,
            message=alert.message,
            threat_level=alert.threat_level.value,
            is_sent=alert.is_sent,
            sent_at=alert.sent_at.isoformat() if alert.sent_at else None,
            sent_channels=alert.sent_channels,
            created_at=alert.created_at.isoformat()
        )
        for alert in alerts
    ]


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get a specific alert"""
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return AlertResponse(
        id=alert.id,
        breach_data_id=alert.breach_data_id,
        title=alert.title,
        message=alert.message,
        threat_level=alert.threat_level.value,
        is_sent=alert.is_sent,
        sent_at=alert.sent_at.isoformat() if alert.sent_at else None,
        sent_channels=alert.sent_channels,
        created_at=alert.created_at.isoformat()
    )