"""
LegacyAI Database & SQL Repository Test Suite
Validates SQLAlchemy ORM models, database seeding, JOINs, GROUP BY aggregations, and decision log persistence.
"""

import os
import pytest
from backend.db.database import SessionLocal, init_db, engine, Base
from backend.db.models import User, Account, Asset, Holding, Transaction, DecisionLog
from backend.db.seed import seed_database
from backend.db.repositories import (
    PortfolioRepository, 
    TransactionRepository, 
    DecisionLogRepository
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample")

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Initializes database and seeds test records."""
    init_db()
    seed_database(data_dir=DATA_DIR)
    yield
    # Teardown: we keep the data for development inspection

def test_database_tables_seeded():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        assert len(users) >= 2
        user_ids = [u.id for u in users]
        assert "usr_001" in user_ids

        accounts = db.query(Account).filter(Account.user_id == "usr_001").all()
        assert len(accounts) >= 2

        holdings = db.query(Holding).filter(Holding.user_id == "usr_001").all()
        assert len(holdings) == 7

        transactions = db.query(Transaction).filter(Transaction.user_id == "usr_001").all()
        assert len(transactions) > 50

        assets = db.query(Asset).all()
        assert len(assets) >= 7
    finally:
        db.close()

def test_portfolio_repository_join():
    """Validates inner JOIN between Holdings and Asset table."""
    db = SessionLocal()
    try:
        repo = PortfolioRepository(db)
        enriched_holdings = repo.get_user_portfolio_holdings("usr_001")
        
        assert len(enriched_holdings) == 7
        # Verify columns from both tables are present
        first = enriched_holdings[0]
        assert "ticker" in first
        assert "asset_name" in first
        assert "market_value" in first
        assert "unrealized_gain_loss" in first
        assert first["market_value"] > 0
    finally:
        db.close()

def test_portfolio_repository_aggregation():
    """Validates GROUP BY and SUM aggregations for asset class breakdown."""
    db = SessionLocal()
    try:
        repo = PortfolioRepository(db)
        allocations = repo.get_asset_allocation_summary("usr_001")
        
        assert len(allocations) >= 3
        asset_classes = [a["asset_class"] for a in allocations]
        assert "EQUITY" in asset_classes
        assert "FIXED_INCOME" in asset_classes

        # Verify aggregate sum values
        equity_alloc = next(a for a in allocations if a["asset_class"] == "EQUITY")
        assert equity_alloc["total_market_value"] > 100000.0
        assert equity_alloc["position_count"] >= 3

        cash = repo.get_user_total_cash("usr_001")
        assert cash > 0.0
    finally:
        db.close()

def test_transaction_repository_category_spending():
    """Validates GROUP BY and HAVING filters on category spending."""
    db = SessionLocal()
    try:
        repo = TransactionRepository(db)
        spending = repo.get_category_spending("usr_001")
        
        assert len(spending) > 0
        categories = [s["category"] for s in spending]
        assert "HOUSING" in categories
        
        # Housing should have positive sum
        housing = next(s for s in spending if s["category"] == "HOUSING")
        assert housing["total_amount"] >= 3200.0
        assert housing["transaction_count"] >= 1
    finally:
        db.close()

def test_transaction_repository_cashflow_totals():
    """Validates total debits, total credits, and net cash flow computation."""
    db = SessionLocal()
    try:
        repo = TransactionRepository(db)
        cf = repo.get_monthly_cash_flow_totals("usr_001")
        
        assert cf["total_income"] > 0.0
        assert cf["total_expenses"] > 0.0
        assert cf["net_cash_flow"] != 0.0
    finally:
        db.close()

def test_transaction_repository_large_outliers():
    """Validates parameterized filtering for large transactions."""
    db = SessionLocal()
    try:
        repo = TransactionRepository(db)
        large_txs = repo.get_large_transactions("usr_001", threshold=3000.0)
        
        assert len(large_txs) >= 2 # Housing rent and luxury watch purchase
        amounts = [t["amount"] for t in large_txs]
        assert all(amt >= 3000.0 for amt in amounts)
    finally:
        db.close()

import uuid

def test_decision_log_repository_persistence():
    """Validates recording and retrieving immutable audit decision logs."""
    db = SessionLocal()
    try:
        repo = DecisionLogRepository(db)
        test_id = f"dec_test_{uuid.uuid4().hex[:8]}"
        # Record a test decision
        log = repo.record_decision(
            decision_id=test_id,
            user_id="usr_001",
            query="Simulate inflation at 6% over 10 years",
            intent="INFLATION_SCENARIO",
            tools_called='["calculate_inflation_impact"]',
            calculations='{"final_purchasing_power": 55839.48, "loss_pct": 44.16}',
            sources_cited='[{"source": "Bureau of Labor Statistics CPI", "page": 3}]',
            model_confidence=0.99,
            execution_time_ms=88.4
        )
        assert log.id == test_id

        # Query recent decisions
        recent = repo.get_recent_decisions("usr_001", limit=5)
        assert len(recent) >= 2
        decision_ids = [d.id for d in recent]
        assert test_id in decision_ids
        
        fetched = next(d for d in recent if d.id == test_id)
        assert fetched.intent == "INFLATION_SCENARIO"
        assert "calculate_inflation_impact" in fetched.tools_called
    finally:
        db.close()
