"""
Database configuration and connection management
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
import redis.asyncio as redis
from typing import AsyncGenerator
import asyncio

from config.settings import settings


# PostgreSQL Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,
    echo=settings.DEBUG,
    future=True
)

# Session factory
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Redis connection
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session"""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_redis() -> redis.Redis:
    """Dependency for getting Redis client"""
    return redis_client


async def init_db():
    """Initialize database tables"""
    from app.models.database import Base
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections"""
    await engine.dispose()
    await redis_client.close()


# Database utilities
class DatabaseManager:
    """Database management utilities"""
    
    @staticmethod
    async def health_check() -> dict:
        """Check database connectivity"""
        try:
            async with async_session_maker() as session:
                result = await session.execute("SELECT 1")
                postgres_status = "healthy" if result else "unhealthy"
        except Exception as e:
            postgres_status = f"error: {str(e)}"
        
        try:
            await redis_client.ping()
            redis_status = "healthy"
        except Exception as e:
            redis_status = f"error: {str(e)}"
        
        return {
            "postgres": postgres_status,
            "redis": redis_status
        }
    
    @staticmethod
    async def get_stats() -> dict:
        """Get database statistics"""
        from app.models.database import MonitoringSource, BreachData, Alert
        
        async with async_session_maker() as session:
            try:
                # Get counts
                sources_count = await session.execute(
                    "SELECT COUNT(*) FROM monitoring_sources WHERE status = 'active'"
                )
                breaches_count = await session.execute(
                    "SELECT COUNT(*) FROM breach_data"
                )
                alerts_count = await session.execute(
                    "SELECT COUNT(*) FROM alerts WHERE is_sent = true"
                )
                
                return {
                    "active_sources": sources_count.scalar() or 0,
                    "total_breaches": breaches_count.scalar() or 0,
                    "alerts_sent": alerts_count.scalar() or 0
                }
            except Exception as e:
                return {"error": str(e)}