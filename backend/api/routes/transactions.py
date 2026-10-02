"""
Transactions & Cash Flow Routes
Exposes spending velocity, category totals, net cash flow, and risk anomaly detection.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.repositories import TransactionRepository
from backend.api.schemas import TransactionAnalysisResponse, CategorySpendingItem

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.get("/{user_id}", response_model=TransactionAnalysisResponse)
def get_user_transactions_summary(user_id: str, db: Session = Depends(get_db)):
    repo = TransactionRepository(db)
    category_summary = repo.get_category_spending(user_id)
    if not category_summary:
        raise HTTPException(status_code=404, detail=f"No transaction records found for user: {user_id}")

    cash_flow = repo.get_monthly_cash_flow_totals(user_id)
    large_txs = repo.get_large_transactions(user_id, threshold=2500.0)

    total_income = cash_flow["total_income"]
    total_expenses = cash_flow["total_expenses"]
    net_cf = cash_flow["net_cash_flow"]
    savings_rate = (net_cf / total_income * 100.0) if total_income > 0 else 0.0

    spending_items = [
        CategorySpendingItem(
            category=c["category"],
            total_amount=round(c["total_amount"], 2),
            transaction_count=c["transaction_count"],
            average_ticket_size=round(c["average_ticket_size"], 2)
        )
        for c in category_summary
    ]

    formatted_large_txs = [
        {
            "id": t["id"],
            "date": t["date"].strftime("%Y-%m-%d") if hasattr(t["date"], "strftime") else str(t["date"]),
            "merchant": t["merchant"],
            "category": t["category"],
            "amount": round(t["amount"], 2),
            "type": t["type"]
        }
        for t in large_txs
    ]

    return TransactionAnalysisResponse(
        user_id=user_id,
        total_income=round(total_income, 2),
        total_expenses=round(total_expenses, 2),
        net_cash_flow=round(net_cf, 2),
        savings_rate_pct=round(savings_rate, 2),
        category_spending=spending_items,
        recent_large_transactions=formatted_large_txs
    )
