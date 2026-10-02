"""
LegacyAI Cash Flow and Transaction Analytics Engine
Analyzes spending velocity, category breakdowns, savings rate, recurring bills, and statistical cash flow anomalies using Pandas & NumPy.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd

def analyze_cash_flow(transactions_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes comprehensive cash flow metrics: total income, total burn, net savings, category allocations,
    and statistical outliers.
    """
    if transactions_df.empty:
        return {
            "total_income": 0.0,
            "total_expenses": 0.0,
            "net_cash_flow": 0.0,
            "savings_rate_pct": 0.0,
            "category_breakdown": {},
            "monthly_burn_rate": 0.0,
            "recurring_expenses_monthly": 0.0,
            "anomalies": []
        }

    df = transactions_df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Separate income (CREDIT) and expenses (DEBIT)
    credits = df[df["type"] == "CREDIT"]
    debits = df[df["type"] == "DEBIT"]

    total_income = float(credits["amount"].sum())
    total_expenses = float(debits["amount"].sum())
    net_cash_flow = total_income - total_expenses
    savings_rate = (net_cash_flow / total_income * 100.0) if total_income > 0 else 0.0

    # Category breakdown (expenses only)
    category_summary = debits.groupby("category")["amount"].sum().sort_values(ascending=False)
    category_breakdown = {}
    for cat, amt in category_summary.items():
        category_breakdown[str(cat)] = {
            "amount": round(float(amt), 2),
            "percentage": round(float(amt / total_expenses * 100.0), 2) if total_expenses > 0 else 0.0
        }

    # Monthly breakdown
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    monthly_debits = df[df["type"] == "DEBIT"].groupby("year_month")["amount"].sum()
    monthly_credits = df[df["type"] == "CREDIT"].groupby("year_month")["amount"].sum()
    
    avg_monthly_burn = float(monthly_debits.mean()) if not monthly_debits.empty else 0.0
    
    # Recurring expenses
    recurring_debits = debits[debits["is_recurring"] == 1]
    # monthly average of recurring expenses
    months_count = max(1, len(monthly_debits))
    recurring_monthly = float(recurring_debits["amount"].sum() / months_count)

    # Statistical outlier detection using Z-score on debits (amounts > mean + 2.5 * std)
    anomalies = []
    if len(debits) > 10:
        amounts = debits["amount"].values
        mean_amt = np.mean(amounts)
        std_amt = np.std(amounts)
        threshold = mean_amt + (2.2 * std_amt)
        outlier_rows = debits[debits["amount"] > threshold]

        for _, row in outlier_rows.iterrows():
            z_score = (row["amount"] - mean_amt) / std_amt if std_amt > 0 else 0.0
            anomalies.append({
                "transaction_id": row["transaction_id"],
                "date": str(row["date"].strftime("%Y-%m-%d")),
                "merchant": row["merchant"],
                "category": row["category"],
                "amount": round(float(row["amount"]), 2),
                "z_score": round(float(z_score), 2),
                "flag": "HIGH_MAGNITUDE_UNUSUAL_EXPENSE"
            })

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_cash_flow": round(net_cash_flow, 2),
        "savings_rate_pct": round(savings_rate, 2),
        "category_breakdown": category_breakdown,
        "monthly_burn_rate": round(avg_monthly_burn, 2),
        "recurring_expenses_monthly": round(recurring_monthly, 2),
        "transactions_analyzed": int(len(df)),
        "anomalies": anomalies
    }
