"""
LegacyAI Analytics Engine Test Suite
Validates mathematical integrity of portfolio calculations, cash flow velocity, anomaly detection, and scenario engines.
"""

import os
import pytest
import numpy as np
import pandas as pd

from backend.data.loaders import (
    load_users, 
    load_accounts, 
    load_assets, 
    load_holdings, 
    load_transactions, 
    load_prices
)
from backend.analytics.portfolio_engine import (
    calculate_portfolio_summary, 
    calculate_portfolio_risk_metrics
)
from backend.analytics.cashflow_engine import analyze_cash_flow
from backend.analytics.scenario_engine import (
    calculate_inflation_impact, 
    simulate_macro_shock, 
    run_monte_carlo_simulation
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample")

def test_data_loaders():
    users = load_users(DATA_DIR)
    assert not users.empty
    assert "usr_001" in users["user_id"].values

    accounts = load_accounts(DATA_DIR, user_id="usr_001")
    assert len(accounts) >= 2

    holdings = load_holdings(DATA_DIR, user_id="usr_001")
    assert len(holdings) == 7
    assert "SPY" in holdings["ticker"].values

    transactions = load_transactions(DATA_DIR, user_id="usr_001")
    assert len(transactions) > 50

    prices = load_prices(DATA_DIR, ticker="SPY")
    assert len(prices) > 100

def test_portfolio_summary():
    holdings = load_holdings(DATA_DIR, user_id="usr_001")
    cash_bal = 28460.00
    summary = calculate_portfolio_summary(holdings, cash_balance=cash_bal)

    # Validate portfolio total is in the expected ~$284k realm
    assert summary["total_value"] > 250000.0
    assert summary["invested_value"] > 200000.0
    assert summary["cash_balance"] == cash_bal
    assert "EQUITY" in summary["asset_allocation"]
    assert "FIXED_INCOME" in summary["asset_allocation"]
    assert summary["holdings_count"] == 7
    # HHI concentration should be bounded between 0 and 1
    assert 0.0 < summary["hhi_concentration"] <= 1.0

def test_portfolio_risk_metrics():
    holdings = load_holdings(DATA_DIR, user_id="usr_001")
    prices = load_prices(DATA_DIR)
    risk = calculate_portfolio_risk_metrics(holdings, prices)

    # Volatility should be realistic (e.g. 5% to 35%)
    assert 5.0 <= risk["annualized_volatility_pct"] <= 40.0
    assert risk["var_95_1d_pct"] > 0.0
    assert risk["var_95_1d_dollars"] > 0.0

def test_cashflow_engine_and_anomalies():
    transactions = load_transactions(DATA_DIR, user_id="usr_001")
    cf = analyze_cash_flow(transactions)

    assert cf["total_income"] > 0.0
    assert cf["total_expenses"] > 0.0
    assert cf["savings_rate_pct"] > 0.0
    assert "HOUSING" in cf["category_breakdown"]
    assert cf["monthly_burn_rate"] > 0.0

    # Test statistical anomaly detection caught our intentionally injected large transactions
    anomalies = cf["anomalies"]
    assert len(anomalies) >= 2
    merchants = [a["merchant"] for a in anomalies]
    assert any("Rolex" in m for m in merchants)
    assert any("Jet" in m for m in merchants)

def test_inflation_calculator():
    amount = 100000.0
    res = calculate_inflation_impact(amount, annual_inflation_rate=0.05, years=5)

    assert res["initial_amount"] == 100000.0
    assert res["years"] == 5
    # Purchasing power should strictly decrease
    assert res["final_purchasing_power"] < amount
    # Mathematical formula check: 100000 / (1.05^5) = 78352.62
    expected = 100000.0 / (1.05 ** 5)
    assert pytest.approx(res["final_purchasing_power"], rel=1e-2) == expected

def test_macro_shock_simulation():
    res = simulate_macro_shock(
        portfolio_value=284620.0,
        equity_weight=0.61,
        bond_weight=0.24,
        cash_weight=0.10,
        shock_type="INFLATION_SURGE"
    )

    assert res["initial_portfolio_value"] == 284620.0
    assert res["post_shock_value"] < res["initial_portfolio_value"]
    assert res["net_dollar_impact"] < 0
    assert "equity_change_dollars" in res["asset_level_impact"]

def test_monte_carlo_simulation():
    res = run_monte_carlo_simulation(
        initial_investment=50000.0,
        monthly_contribution=1500.0,
        expected_annual_return=0.08,
        annual_volatility=0.15,
        years=10,
        iterations=500
    )

    assert res["years"] == 10
    # Optimistic p90 should be strictly greater than median p50 and conservative p10
    assert res["optimistic_p90"] > res["median_outcome_p50"] > res["conservative_p10"]
    assert len(res["timeline"]) == 11 # Year 0 to 10
