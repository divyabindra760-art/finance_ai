"""
Health Check Route
Provides API status and database connectivity heartbeat.
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.db.database import get_db
from backend.api.schemas import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
def get_health(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return HealthResponse(
        status="healthy",
        version="2.0.0",
        service="LegacyAI Financial Intelligence API",
        database_status=db_status,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )
