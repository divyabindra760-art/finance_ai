"""
Portfolio Routes
Exposes enriched holdings, aggregate asset allocations, and total valuation via SQL queries.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.repositories import PortfolioRepository
from backend.api.schemas import PortfolioResponse, HoldingItem, AssetAllocationItem

router = APIRouter(prefix="/api/portfolio", tags=["Portfolio"])

@router.get("/{user_id}", response_model=PortfolioResponse)
def get_user_portfolio(user_id: str, db: Session = Depends(get_db)):
    repo = PortfolioRepository(db)
    raw_holdings = repo.get_user_portfolio_holdings(user_id)
    if not raw_holdings:
        raise HTTPException(status_code=404, detail=f"No portfolio holdings found for user: {user_id}")

    raw_allocations = repo.get_asset_allocation_summary(user_id)
    cash_bal = repo.get_user_total_cash(user_id)

    invested_val = sum(h["market_value"] for h in raw_holdings)
    total_val = invested_val + cash_bal

    holdings_items = [
        HoldingItem(
            id=h["id"],
            ticker=h["ticker"],
            asset_name=h["asset_name"],
            asset_class=h["asset_class"],
            quantity=h["quantity"],
            average_cost=h["average_cost"],
            current_price=h["current_price"],
            market_value=round(h["market_value"], 2),
            unrealized_gain_loss=round(h["unrealized_gain_loss"], 2),
            gain_loss_pct=round(h["gain_loss_pct"], 2)
        )
        for h in raw_holdings
    ]

    alloc_items = [
        AssetAllocationItem(
            asset_class=a["asset_class"],
            total_market_value=round(a["total_market_value"], 2),
            position_count=a["position_count"]
        )
        for a in raw_allocations
    ]
    if cash_bal > 0:
        alloc_items.append(AssetAllocationItem(
            asset_class="CASH",
            total_market_value=round(cash_bal, 2),
            position_count=1
        ))

    return PortfolioResponse(
        user_id=user_id,
        total_portfolio_value=round(total_val, 2),
        invested_value=round(invested_val, 2),
        cash_balance=round(cash_bal, 2),
        holdings_count=len(holdings_items),
        asset_allocations=alloc_items,
        holdings=holdings_items
    )
