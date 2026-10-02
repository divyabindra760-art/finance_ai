"""
LegacyAI SQL Repository Layer
Demonstrates production-grade SQL concepts: JOINs, GROUP BY, HAVING, subqueries, and aggregations using SQLAlchemy 2.0.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy import func, desc, and_, select
from sqlalchemy.orm import Session
from backend.db.models import (
    User, 
    Account, 
    Asset, 
    Holding, 
    Transaction, 
    MarketPrice, 
    DecisionLog
)

class PortfolioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_portfolio_holdings(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Executes an inner JOIN between Holdings and Asset master table to fetch enriched portfolio holdings.
        Demonstrates: SELECT, JOIN, WHERE, ORDER BY
        """
        stmt = (
            select(
                Holding.id,
                Holding.ticker,
                Asset.name.label("asset_name"),
                Holding.asset_class,
                Holding.quantity,
                Holding.average_cost,
                Holding.current_price,
                Holding.market_value,
                ((Holding.current_price - Holding.average_cost) * Holding.quantity).label("unrealized_gain_loss"),
                (((Holding.current_price - Holding.average_cost) / Holding.average_cost) * 100.0).label("gain_loss_pct")
            )
            .join(Asset, Holding.ticker == Asset.ticker)
            .where(Holding.user_id == user_id)
            .order_by(desc(Holding.market_value))
        )
        results = self.db.execute(stmt).all()
        return [dict(r._mapping) for r in results]

    def get_asset_allocation_summary(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Computes aggregate market values per asset class.
        Demonstrates: SELECT, GROUP BY, SUM, HAVING
        """
        stmt = (
            select(
                Holding.asset_class,
                func.sum(Holding.market_value).label("total_market_value"),
                func.count(Holding.id).label("position_count")
            )
            .where(Holding.user_id == user_id)
            .group_by(Holding.asset_class)
            .having(func.sum(Holding.market_value) > 0)
            .order_by(desc("total_market_value"))
        )
        results = self.db.execute(stmt).all()
        return [dict(r._mapping) for r in results]

    def get_user_total_cash(self, user_id: str) -> float:
        """Computes aggregate cash balance across all liquid accounts."""
        stmt = select(func.sum(Account.cash_balance)).where(Account.user_id == user_id)
        val = self.db.execute(stmt).scalar()
        return float(val) if val is not None else 0.0


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_category_spending(
        self, 
        user_id: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Computes spending totals and counts per merchant category.
        Demonstrates: SELECT, WHERE, GROUP BY, HAVING, ORDER BY
        """
        conditions = [
            Transaction.user_id == user_id,
            Transaction.type == "DEBIT"
        ]
        if start_date:
            conditions.append(Transaction.date >= start_date)
        if end_date:
            conditions.append(Transaction.date <= end_date)

        stmt = (
            select(
                Transaction.category,
                func.sum(Transaction.amount).label("total_amount"),
                func.count(Transaction.id).label("transaction_count"),
                func.avg(Transaction.amount).label("average_ticket_size")
            )
            .where(and_(*conditions))
            .group_by(Transaction.category)
            .having(func.sum(Transaction.amount) > 0)
            .order_by(desc("total_amount"))
        )
        results = self.db.execute(stmt).all()
        return [dict(r._mapping) for r in results]

    def get_monthly_cash_flow_totals(self, user_id: str) -> Dict[str, float]:
        """
        Computes total debits vs total credits for a user.
        Demonstrates: conditional aggregations with SUM and WHERE
        """
        credit_stmt = select(func.sum(Transaction.amount)).where(
            and_(Transaction.user_id == user_id, Transaction.type == "CREDIT")
        )
        debit_stmt = select(func.sum(Transaction.amount)).where(
            and_(Transaction.user_id == user_id, Transaction.type == "DEBIT")
        )
        total_income = float(self.db.execute(credit_stmt).scalar() or 0.0)
        total_expenses = float(self.db.execute(debit_stmt).scalar() or 0.0)
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_cash_flow": total_income - total_expenses
        }

    def get_large_transactions(self, user_id: str, threshold: float = 2000.0) -> List[Dict[str, Any]]:
        """
        Finds transactions exceeding an institutional risk threshold.
        Demonstrates: parameterized filtering with order by date desc
        """
        stmt = (
            select(
                Transaction.id,
                Transaction.date,
                Transaction.merchant,
                Transaction.category,
                Transaction.amount,
                Transaction.type
            )
            .where(and_(Transaction.user_id == user_id, Transaction.amount >= threshold))
            .order_by(desc(Transaction.date))
        )
        results = self.db.execute(stmt).all()
        return [dict(r._mapping) for r in results]


class DecisionLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def record_decision(
        self,
        decision_id: str,
        user_id: str,
        query: str,
        intent: str,
        tools_called: str,
        calculations: str,
        sources_cited: str,
        model_confidence: float = 1.0,
        execution_time_ms: float = 0.0
    ) -> DecisionLog:
        """Inserts an auditable immutable decision record into the database."""
        log = DecisionLog(
            id=decision_id,
            user_id=user_id,
            timestamp=datetime.utcnow(),
            query=query,
            intent=intent,
            tools_called=tools_called,
            calculations=calculations,
            sources_cited=sources_cited,
            model_confidence=model_confidence,
            execution_time_ms=execution_time_ms
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_recent_decisions(self, user_id: str, limit: int = 10) -> List[DecisionLog]:
        """Retrieves recent decision records for the audit trail."""
        stmt = (
            select(DecisionLog)
            .where(DecisionLog.user_id == user_id)
            .order_by(desc(DecisionLog.timestamp))
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())
