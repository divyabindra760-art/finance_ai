"""
Decision Log & Audit Routes
Exposes immutable AI recommendation traces, tools called, calculations, and citations.
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.repositories import DecisionLogRepository
from backend.api.schemas import DecisionLogItem

router = APIRouter(prefix="/api/decisions", tags=["Decision Logs"])

@router.get("/{user_id}", response_model=List[DecisionLogItem])
def get_user_decision_logs(
    user_id: str, 
    limit: int = Query(default=10, ge=1, le=50), 
    db: Session = Depends(get_db)
):
    repo = DecisionLogRepository(db)
    logs = repo.get_recent_decisions(user_id=user_id, limit=limit)
    return [
        DecisionLogItem(
            id=log.id,
            user_id=log.user_id,
            timestamp=log.timestamp.isoformat() if hasattr(log.timestamp, "isoformat") else str(log.timestamp),
            query=log.query,
            intent=log.intent,
            tools_called=log.tools_called,
            calculations=log.calculations,
            sources_cited=log.sources_cited,
            model_confidence=log.model_confidence,
            execution_time_ms=log.execution_time_ms
        )
        for log in logs
    ]
