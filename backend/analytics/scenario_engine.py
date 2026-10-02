"""
LegacyAI Scenario Analysis and Stress-Testing Engine
Deterministic and stochastic simulations using NumPy:
- Inflation purchasing power decay
- Interest rate shock impact on bond valuation (Duration approximation)
- Equity market drawdowns
- Monte Carlo portfolio projections
"""

from typing import Dict, Any, List
import numpy as np

def calculate_inflation_impact(amount: float, annual_inflation_rate: float, years: int) -> Dict[str, Any]:
    """
    Computes real purchasing power degradation over time:
    Real Value = Nominal Amount / (1 + r)^t
    """
    timeline = []
    r = annual_inflation_rate
    
    for t in range(years + 1):
        nominal = amount
        purchasing_power = amount / ((1.0 + r) ** t)
        purchasing_power_loss = nominal - purchasing_power
        loss_pct = (purchasing_power_loss / nominal) * 100.0
        
        timeline.append({
            "year": t,
            "nominal_value": round(nominal, 2),
            "real_purchasing_power": round(purchasing_power, 2),
            "cumulative_loss": round(purchasing_power_loss, 2),
            "purchasing_power_loss_pct": round(loss_pct, 2)
        })

    total_loss = amount - (amount / ((1.0 + r) ** years))
    
    return {
        "initial_amount": round(amount, 2),
        "annual_inflation_rate_pct": round(annual_inflation_rate * 100.0, 2),
        "years": years,
        "final_purchasing_power": round(timeline[-1]["real_purchasing_power"], 2),
        "cumulative_purchasing_power_loss": round(total_loss, 2),
        "loss_percentage": round((total_loss / amount) * 100.0, 2),
        "timeline": timeline
    }

def simulate_macro_shock(
    portfolio_value: float,
    equity_weight: float,
    bond_weight: float,
    cash_weight: float,
    shock_type: str = "INFLATION_SURGE"
) -> Dict[str, Any]:
    """
    Simulates macro shocks:
    - INFLATION_SURGE: +300bps inflation, yields +200bps, equities -12%, bonds -8% (effective duration ~4.2)
    - RATE_HIKE: Fed hikes +200bps, equities -15%, bonds -10%
    - MARKET_DRAWDOWN: Equities -25%, bonds +4% (flight to safety), cash unaffected
    - STAGFLATION: Equities -20%, bonds -12%, commodities/cash hedge
    """
    shocks = {
        "INFLATION_SURGE": {
            "name": "Sudden Inflation Surge (+3.5%)",
            "equity_return": -0.12,
            "bond_return": -0.08,
            "cash_return": 0.045
        },
        "RATE_HIKE": {
            "name": "Aggressive Central Bank Rate Hike (+200 bps)",
            "equity_return": -0.15,
            "bond_return": -0.10,
            "cash_return": 0.05
        },
        "MARKET_DRAWDOWN": {
            "name": "Severe Equity Market Correction (-25%)",
            "equity_return": -0.25,
            "bond_return": 0.04,
            "cash_return": 0.0
        },
        "STAGFLATION": {
            "name": "1970s Style Stagflation Regime",
            "equity_return": -0.20,
            "bond_return": -0.12,
            "cash_return": -0.06 # negative real cash return
        }
    }

    shock_params = shocks.get(shock_type, shocks["INFLATION_SURGE"])
    
    equity_val = portfolio_value * equity_weight
    bond_val = portfolio_value * bond_weight
    cash_val = portfolio_value * cash_weight
    other_val = portfolio_value * max(0.0, 1.0 - (equity_weight + bond_weight + cash_weight))

    shocked_equity = equity_val * (1.0 + shock_params["equity_return"])
    shocked_bond = bond_val * (1.0 + shock_params["bond_return"])
    shocked_cash = cash_val * (1.0 + shock_params["cash_return"])
    shocked_other = other_val * 0.95 # mild discount

    post_shock_value = shocked_equity + shocked_bond + shocked_cash + shocked_other
    value_change = post_shock_value - portfolio_value
    pct_change = (value_change / portfolio_value) * 100.0

    return {
        "shock_type": shock_type,
        "scenario_name": shock_params["name"],
        "initial_portfolio_value": round(portfolio_value, 2),
        "post_shock_value": round(post_shock_value, 2),
        "net_dollar_impact": round(value_change, 2),
        "percentage_impact": round(pct_change, 2),
        "asset_level_impact": {
            "equity_change_dollars": round(shocked_equity - equity_val, 2),
            "bond_change_dollars": round(shocked_bond - bond_val, 2),
            "cash_change_dollars": round(shocked_cash - cash_val, 2)
        }
    }

def run_monte_carlo_simulation(
    initial_investment: float,
    monthly_contribution: float,
    expected_annual_return: float,
    annual_volatility: float,
    years: int = 10,
    iterations: int = 1000
) -> Dict[str, Any]:
    """
    Monte Carlo stochastic simulation using geometric Brownian motion with NumPy:
    S_t = S_0 * exp((mu - 0.5 * sigma^2)*dt + sigma * sqrt(dt) * Z)
    """
    np.random.seed(42)
    months = years * 12
    dt = 1.0 / 12.0
    mu = expected_annual_return
    sigma = annual_volatility
    
    # Generate random standard normals for all simulations and months
    shocks = np.random.normal(0, 1, size=(iterations, months))
    
    monthly_drift = (mu - 0.5 * (sigma ** 2)) * dt
    monthly_diffusion = sigma * np.sqrt(dt) * shocks
    monthly_multipliers = np.exp(monthly_drift + monthly_diffusion)

    trajectories = np.zeros((iterations, months + 1))
    trajectories[:, 0] = initial_investment

    for m in range(1, months + 1):
        # Compound previous month + apply monthly multiplier + add new contribution
        trajectories[:, m] = (trajectories[:, m - 1] * monthly_multipliers[:, m - 1]) + monthly_contribution

    # Extract statistical percentiles
    final_values = trajectories[:, -1]
    p10 = float(np.percentile(final_values, 10))
    p50 = float(np.percentile(final_values, 50)) # median
    p90 = float(np.percentile(final_values, 90))

    total_contributed = initial_investment + (monthly_contribution * months)

    # Sample trajectory curves for frontend charting (yearly intervals)
    sample_indices = np.linspace(0, months, years + 1, dtype=int)
    yearly_p10 = np.percentile(trajectories[:, sample_indices], 10, axis=0)
    yearly_p50 = np.percentile(trajectories[:, sample_indices], 50, axis=0)
    yearly_p90 = np.percentile(trajectories[:, sample_indices], 90, axis=0)

    timeline = []
    for yr_idx, yr in enumerate(range(years + 1)):
        timeline.append({
            "year": yr,
            "bear_p10": round(float(yearly_p10[yr_idx]), 2),
            "median_p50": round(float(yearly_p50[yr_idx]), 2),
            "bull_p90": round(float(yearly_p90[yr_idx]), 2)
        })

    return {
        "initial_investment": round(initial_investment, 2),
        "monthly_contribution": round(monthly_contribution, 2),
        "total_principal_contributed": round(total_contributed, 2),
        "years": years,
        "iterations": iterations,
        "median_outcome_p50": round(p50, 2),
        "conservative_p10": round(p10, 2),
        "optimistic_p90": round(p90, 2),
        "timeline": timeline
    }
