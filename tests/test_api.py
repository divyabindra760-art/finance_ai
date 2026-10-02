"""
LegacyAI FastAPI REST API Test Suite
Automated endpoint validation using Starlette TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.database import init_db
from backend.db.seed import seed_database

@pytest.fixture(scope="module", autouse=True)
def prepare_test_api():
    init_db()
    seed_database()

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["version"] == "2.0.0"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database_status"] == "connected"

def test_get_portfolio_valid_user():
    response = client.get("/api/portfolio/usr_001")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "usr_001"
    assert data["total_portfolio_value"] > 250000.0
    assert data["holdings_count"] == 7
    assert len(data["asset_allocations"]) >= 3
    # Check that holdings contain essential metrics
    first_holding = data["holdings"][0]
    assert "ticker" in first_holding
    assert "market_value" in first_holding
    assert "gain_loss_pct" in first_holding

def test_get_portfolio_unknown_user():
    response = client.get("/api/portfolio/usr_nonexistent")
    assert response.status_code == 404

def test_get_transactions_summary():
    response = client.get("/api/transactions/usr_001")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "usr_001"
    assert data["total_income"] > 0
    assert data["total_expenses"] > 0
    assert data["savings_rate_pct"] > 0
    assert len(data["category_spending"]) > 0

def test_simulate_inflation_endpoint():
    payload = {
        "amount": 100000.0,
        "annual_inflation_rate": 0.05,
        "years": 5
    }
    response = client.post("/api/scenarios/inflation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["initial_amount"] == 100000.0
    assert data["final_purchasing_power"] < 100000.0
    assert len(data["timeline"]) == 6 # Year 0 to 5

def test_simulate_macro_shock_endpoint():
    payload = {
        "portfolio_value": 284620.0,
        "equity_weight": 0.61,
        "bond_weight": 0.24,
        "cash_weight": 0.10,
        "shock_type": "RATE_HIKE"
    }
    response = client.post("/api/scenarios/macro-shock", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["shock_type"] == "RATE_HIKE"
    assert data["post_shock_value"] < 284620.0
    assert "net_dollar_impact" in data

def test_simulate_monte_carlo_endpoint():
    payload = {
        "initial_investment": 25000.0,
        "monthly_contribution": 1000.0,
        "expected_annual_return": 0.08,
        "annual_volatility": 0.15,
        "years": 5,
        "iterations": 200
    }
    response = client.post("/api/scenarios/monte-carlo", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["years"] == 5
    assert data["optimistic_p90"] > data["median_outcome_p50"] > data["conservative_p10"]
    assert len(data["timeline"]) == 6

def test_get_decision_logs():
    response = client.get("/api/decisions/usr_001")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    first_log = data[0]
    assert "id" in first_log
    assert "query" in first_log
    assert "intent" in first_log
