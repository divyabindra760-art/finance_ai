"""
LegacyAI Pydantic Request & Response Schemas
Defines type-safe data transfer objects (DTOs) with strict validation.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "2.0.0"
    service: str = "LegacyAI Financial Intelligence API"
    database_status: str = "connected"
    timestamp: str

class HoldingItem(BaseModel):
    id: str
    ticker: str
    asset_name: str
    asset_class: str
    quantity: float
    average_cost: float
    current_price: float
    market_value: float
    unrealized_gain_loss: float
    gain_loss_pct: float

class AssetAllocationItem(BaseModel):
    asset_class: str
    total_market_value: float
    position_count: int

class PortfolioResponse(BaseModel):
    user_id: str
    total_portfolio_value: float
    invested_value: float
    cash_balance: float
    holdings_count: int
    asset_allocations: List[AssetAllocationItem]
    holdings: List[HoldingItem]

class CategorySpendingItem(BaseModel):
    category: str
    total_amount: float
    transaction_count: int
    average_ticket_size: float

class TransactionAnalysisResponse(BaseModel):
    user_id: str
    total_income: float
    total_expenses: float
    net_cash_flow: float
    savings_rate_pct: float
    category_spending: List[CategorySpendingItem]
    recent_large_transactions: List[Dict[str, Any]]

class InflationRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Nominal principal amount in USD")
    annual_inflation_rate: float = Field(..., ge=0, le=1.0, description="Annual inflation rate (e.g. 0.05 for 5%)")
    years: int = Field(..., ge=1, le=50, description="Time horizon in years")

class InflationYearlyPoint(BaseModel):
    year: int
    nominal_value: float
    real_purchasing_power: float
    cumulative_loss: float
    purchasing_power_loss_pct: float

class InflationResponse(BaseModel):
    initial_amount: float
    annual_inflation_rate_pct: float
    years: int
    final_purchasing_power: float
    cumulative_purchasing_power_loss: float
    loss_percentage: float
    timeline: List[InflationYearlyPoint]

class MacroShockRequest(BaseModel):
    portfolio_value: float = Field(..., gt=0)
    equity_weight: float = Field(default=0.61, ge=0.0, le=1.0)
    bond_weight: float = Field(default=0.24, ge=0.0, le=1.0)
    cash_weight: float = Field(default=0.10, ge=0.0, le=1.0)
    shock_type: str = Field(default="INFLATION_SURGE") # INFLATION_SURGE, RATE_HIKE, MARKET_DRAWDOWN, STAGFLATION

class MacroShockResponse(BaseModel):
    shock_type: str
    scenario_name: str
    initial_portfolio_value: float
    post_shock_value: float
    net_dollar_impact: float
    percentage_impact: float
    asset_level_impact: Dict[str, float]

class MonteCarloRequest(BaseModel):
    initial_investment: float = Field(..., ge=0)
    monthly_contribution: float = Field(default=1000.0, ge=0)
    expected_annual_return: float = Field(default=0.08, ge=-0.5, le=1.0)
    annual_volatility: float = Field(default=0.15, ge=0.01, le=1.0)
    years: int = Field(default=10, ge=1, le=40)
    iterations: int = Field(default=500, ge=50, le=5000)

class MonteCarloTrajectoryPoint(BaseModel):
    year: int
    bear_p10: float
    median_p50: float
    bull_p90: float

class MonteCarloResponse(BaseModel):
    initial_investment: float
    monthly_contribution: float
    total_principal_contributed: float
    years: int
    iterations: int
    median_outcome_p50: float
    conservative_p10: float
    optimistic_p90: float
    timeline: List[MonteCarloTrajectoryPoint]

class DecisionLogItem(BaseModel):
    id: str
    user_id: str
    timestamp: str
    query: str
    intent: str
    tools_called: Optional[str] = None
    calculations: Optional[str] = None
    sources_cited: Optional[str] = None
    model_confidence: float
    execution_time_ms: float
