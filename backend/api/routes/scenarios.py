"""
Scenario & Stress Testing Routes
Executes deterministic purchasing power calculations, macro regime shocks, and NumPy Monte Carlo simulations.
"""

from fastapi import APIRouter
from backend.api.schemas import (
    InflationRequest, 
    InflationResponse, 
    InflationYearlyPoint,
    MacroShockRequest, 
    MacroShockResponse,
    MonteCarloRequest, 
    MonteCarloResponse, 
    MonteCarloTrajectoryPoint
)
from backend.analytics.scenario_engine import (
    calculate_inflation_impact, 
    simulate_macro_shock, 
    run_monte_carlo_simulation
)

router = APIRouter(prefix="/api/scenarios", tags=["Scenarios"])

@router.post("/inflation", response_model=InflationResponse)
def simulate_inflation(req: InflationRequest):
    res = calculate_inflation_impact(
        amount=req.amount,
        annual_inflation_rate=req.annual_inflation_rate,
        years=req.years
    )
    timeline_pts = [
        InflationYearlyPoint(
            year=p["year"],
            nominal_value=p["nominal_value"],
            real_purchasing_power=p["real_purchasing_power"],
            cumulative_loss=p["cumulative_loss"],
            purchasing_power_loss_pct=p["purchasing_power_loss_pct"]
        )
        for p in res["timeline"]
    ]
    return InflationResponse(
        initial_amount=res["initial_amount"],
        annual_inflation_rate_pct=res["annual_inflation_rate_pct"],
        years=res["years"],
        final_purchasing_power=res["final_purchasing_power"],
        cumulative_purchasing_power_loss=res["cumulative_purchasing_power_loss"],
        loss_percentage=res["loss_percentage"],
        timeline=timeline_pts
    )

@router.post("/macro-shock", response_model=MacroShockResponse)
def simulate_shock(req: MacroShockRequest):
    res = simulate_macro_shock(
        portfolio_value=req.portfolio_value,
        equity_weight=req.equity_weight,
        bond_weight=req.bond_weight,
        cash_weight=req.cash_weight,
        shock_type=req.shock_type
    )
    return MacroShockResponse(
        shock_type=res["shock_type"],
        scenario_name=res["scenario_name"],
        initial_portfolio_value=res["initial_portfolio_value"],
        post_shock_value=res["post_shock_value"],
        net_dollar_impact=res["net_dollar_impact"],
        percentage_impact=res["percentage_impact"],
        asset_level_impact=res["asset_level_impact"]
    )

@router.post("/monte-carlo", response_model=MonteCarloResponse)
def simulate_monte_carlo(req: MonteCarloRequest):
    res = run_monte_carlo_simulation(
        initial_investment=req.initial_investment,
        monthly_contribution=req.monthly_contribution,
        expected_annual_return=req.expected_annual_return,
        annual_volatility=req.annual_volatility,
        years=req.years,
        iterations=req.iterations
    )
    timeline_pts = [
        MonteCarloTrajectoryPoint(
            year=t["year"],
            bear_p10=t["bear_p10"],
            median_p50=t["median_p50"],
            bull_p90=t["bull_p90"]
        )
        for t in res["timeline"]
    ]
    return MonteCarloResponse(
        initial_investment=res["initial_investment"],
        monthly_contribution=res["monthly_contribution"],
        total_principal_contributed=res["total_principal_contributed"],
        years=res["years"],
        iterations=res["iterations"],
        median_outcome_p50=res["median_outcome_p50"],
        conservative_p10=res["conservative_p10"],
        optimistic_p90=res["optimistic_p90"],
        timeline=timeline_pts
    )
