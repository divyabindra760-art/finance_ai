import os
import sys

# Ensure root workspace directory is in python search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
from datetime import datetime
from backend.db.database import SessionLocal, init_db
from backend.db.models import (
    User, 
    Account, 
    Asset, 
    Holding, 
    Transaction, 
    MarketPrice, 
    PortfolioSnapshot, 
    DecisionLog
)
from backend.data.loaders import (
    load_users, 
    load_accounts, 
    load_assets, 
    load_holdings, 
    load_transactions, 
    load_prices
)

def seed_database(data_dir: str = None):
    print("Initializing database tables...")
    init_db()
    
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(User).first():
            print("Database already contains data. Skipping re-seed.")
            return

        print("Seeding Users...")
        users_df = load_users(data_dir)
        for _, r in users_df.iterrows():
            db.add(User(
                id=r["user_id"],
                email=r["email"],
                full_name=r["full_name"],
                risk_profile=r["risk_profile"],
                created_at=r["created_at"].to_pydatetime()
            ))
        db.commit()

        print("Seeding Accounts...")
        accounts_df = load_accounts(data_dir)
        for _, r in accounts_df.iterrows():
            db.add(Account(
                id=r["account_id"],
                user_id=r["user_id"],
                name=r["name"],
                type=r["type"],
                currency=r["currency"],
                cash_balance=float(r["cash_balance"])
            ))
        db.commit()

        print("Seeding Assets Master...")
        assets_df = load_assets(data_dir)
        for _, r in assets_df.iterrows():
            db.add(Asset(
                ticker=r["ticker"],
                name=r["name"],
                asset_class=r["asset_class"],
                expense_ratio=float(r["expense_ratio"]),
                base_price=float(r["base_price"]),
                annual_volatility=float(r["annual_volatility"])
            ))
        db.commit()

        print("Seeding Holdings...")
        holdings_df = load_holdings(data_dir)
        for _, r in holdings_df.iterrows():
            db.add(Holding(
                id=r["holding_id"],
                user_id=r["user_id"],
                account_id=r["account_id"],
                ticker=r["ticker"],
                asset_class=r["asset_class"],
                quantity=float(r["quantity"]),
                average_cost=float(r["average_cost"]),
                current_price=float(r["current_price"]),
                market_value=float(r["market_value"])
            ))
        db.commit()

        print("Seeding Transactions...")
        tx_df = load_transactions(data_dir)
        for _, r in tx_df.iterrows():
            db.add(Transaction(
                id=r["transaction_id"],
                user_id=r["user_id"],
                account_id=r["account_id"],
                date=r["date"].to_pydatetime(),
                merchant=r["merchant"],
                category=r["category"],
                amount=float(r["amount"]),
                type=r["type"],
                is_recurring=bool(r["is_recurring"])
            ))
        db.commit()

        print("Seeding Market Prices...")
        prices_df = load_prices(data_dir)
        for _, r in prices_df.iterrows():
            db.add(MarketPrice(
                ticker=r["ticker"],
                date=r["date"].to_pydatetime(),
                close_price=float(r["close_price"]),
                daily_return=float(r["daily_return"])
            ))
        db.commit()

        print("Seeding Initial Portfolio Snapshot...")
        db.add(PortfolioSnapshot(
            user_id="usr_001",
            timestamp=datetime.utcnow(),
            total_value=284620.00,
            invested_value=256160.00,
            cash_balance=28460.00,
            hhi_concentration=0.184,
            equity_pct=61.2,
            fixed_income_pct=24.1,
            cash_pct=10.0
        ))

        print("Seeding Sample Decision Log...")
        db.add(DecisionLog(
            id="dec_001",
            user_id="usr_001",
            timestamp=datetime.utcnow(),
            query="Analyze portfolio asset allocation and interest rate risk",
            intent="PORTFOLIO_RISK_AUDIT",
            tools_called=json.dumps(["analyze_portfolio", "calculate_portfolio_risk_metrics"]),
            calculations=json.dumps({
                "total_value": 284620.00,
                "volatility_annualized": "14.2%",
                "fixed_income_duration": 4.6,
                "sharpe_ratio": 1.28
            }),
            sources_cited=json.dumps([
                {"source": "Federal Reserve Monetary Policy Report", "page": 14}
            ]),
            model_confidence=0.98,
            execution_time_ms=142.5
        ))
        db.commit()

        print("Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
