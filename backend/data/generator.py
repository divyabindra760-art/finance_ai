"""
LegacyAI Synthetic Financial Data Generator
Generates institutional-quality synthetic financial datasets:
- users
- accounts
- assets
- holdings
- transactions
- historical prices
- portfolio snapshots
"""

import os
import csv
import math
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

random.seed(42)

def generate_financial_data(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. USERS
    users = [
        {
            "user_id": "usr_001",
            "full_name": "Eleanor Vance",
            "email": "eleanor.vance@institutional.ai",
            "risk_profile": "MODERATE_AGGRESSIVE",
            "created_at": "2024-01-15T09:30:00Z"
        },
        {
            "user_id": "usr_002",
            "full_name": "Marcus Sterling",
            "email": "marcus.sterling@apexcapital.org",
            "risk_profile": "BALANCED_GROWTH",
            "created_at": "2024-03-22T14:15:00Z"
        }
    ]
    
    users_file = os.path.join(output_dir, "users.csv")
    with open(users_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(users[0].keys()))
        writer.writeheader()
        writer.writerows(users)
        
    # 2. ACCOUNTS
    accounts = [
        {
            "account_id": "acc_001",
            "user_id": "usr_001",
            "name": "Apex Primary Brokerage",
            "type": "TAXABLE_BROKERAGE",
            "currency": "USD",
            "cash_balance": 28460.00
        },
        {
            "account_id": "acc_002",
            "user_id": "usr_001",
            "name": "Silicon Treasury Liquidity",
            "type": "HIGH_YIELD_SAVINGS",
            "currency": "USD",
            "cash_balance": 45000.00
        },
        {
            "account_id": "acc_003",
            "user_id": "usr_002",
            "name": "Founders Operating Account",
            "type": "BUSINESS_CHECKING",
            "currency": "USD",
            "cash_balance": 82000.00
        }
    ]
    
    accounts_file = os.path.join(output_dir, "accounts.csv")
    with open(accounts_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(accounts[0].keys()))
        writer.writeheader()
        writer.writerows(accounts)

    # 3. ASSETS MASTER
    assets = [
        {"ticker": "SPY", "name": "SPDR S&P 500 ETF Trust", "asset_class": "EQUITY", "expense_ratio": 0.0009, "base_price": 542.50, "annual_volatility": 0.16},
        {"ticker": "QQQ", "name": "Invesco QQQ Trust (Nasdaq-100)", "asset_class": "EQUITY", "expense_ratio": 0.0020, "base_price": 478.20, "annual_volatility": 0.22},
        {"ticker": "BND", "name": "Vanguard Total Bond Market ETF", "asset_class": "FIXED_INCOME", "expense_ratio": 0.0003, "base_price": 72.80, "annual_volatility": 0.06},
        {"ticker": "TLT", "name": "iShares 20+ Year Treasury Bond ETF", "asset_class": "FIXED_INCOME", "expense_ratio": 0.0015, "base_price": 93.40, "annual_volatility": 0.14},
        {"ticker": "VNQ", "name": "Vanguard Real Estate ETF", "asset_class": "REAL_ESTATE", "expense_ratio": 0.0012, "base_price": 86.10, "annual_volatility": 0.18},
        {"ticker": "GLD", "name": "SPDR Gold Shares", "asset_class": "COMMODITY", "expense_ratio": 0.0040, "base_price": 224.50, "annual_volatility": 0.15},
        {"ticker": "BIL", "name": "SPDR Bloomberg 1-3 Month T-Bill ETF", "asset_class": "CASH_EQUIVALENT", "expense_ratio": 0.0014, "base_price": 91.65, "annual_volatility": 0.01},
        {"ticker": "NVDA", "name": "NVIDIA Corporation", "asset_class": "EQUITY", "expense_ratio": 0.0, "base_price": 128.40, "annual_volatility": 0.42},
        {"ticker": "MSFT", "name": "Microsoft Corporation", "asset_class": "EQUITY", "expense_ratio": 0.0, "base_price": 448.90, "annual_volatility": 0.20},
        {"ticker": "AAPL", "name": "Apple Inc.", "asset_class": "EQUITY", "expense_ratio": 0.0, "base_price": 224.30, "annual_volatility": 0.21}
    ]

    assets_file = os.path.join(output_dir, "assets.csv")
    with open(assets_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(assets[0].keys()))
        writer.writeheader()
        writer.writerows(assets)

    # 4. HOLDINGS (Realistic portfolio totaling ~$284,620 matching UI exactly)
    # Target allocation: ~61% Equity, ~24% Fixed Income, ~10% Cash, ~5% Commodity/Real Estate
    holdings = [
        {
            "holding_id": "hld_001",
            "user_id": "usr_001",
            "account_id": "acc_001",
            "ticker": "SPY",
            "asset_class": "EQUITY",
            "quantity": 180.0,
            "average_cost": 490.10,
            "current_price": 542.50,
            "market_value": round(180.0 * 542.50, 2)
        },
        {
            "holding_id": "hld_002",
            "user_id": "usr_001",
            "account_id": "acc_001",
            "ticker": "QQQ",
            "asset_class": "EQUITY",
            "quantity": 110.0,
            "average_cost": 420.30,
            "current_price": 478.20,
            "market_value": round(110.0 * 478.20, 2)
        },
        {
            "holding_id": "hld_003",
            "user_id": "usr_001",
            "account_id": "acc_001",
            "ticker": "NVDA",
            "asset_class": "EQUITY",
            "quantity": 180.0,
            "average_cost": 95.40,
            "current_price": 128.40,
            "market_value": round(180.0 * 128.40, 2)
        },
        {
            "holding_id": "hld_004",
            "user_id": "usr_001",
            "account_id": "acc_001",
            "ticker": "BND",
            "asset_class": "FIXED_INCOME",
            "quantity": 600.0,
            "average_cost": 71.50,
            "current_price": 72.80,
            "market_value": round(600.0 * 72.80, 2)
        },
        {
            "holding_id": "hld_005",
            "user_id": "usr_001",
            "account_id": "acc_001",
            "ticker": "TLT",
            "asset_class": "FIXED_INCOME",
            "quantity": 260.0,
            "average_cost": 95.80,
            "current_price": 93.40,
            "market_value": round(260.0 * 93.40, 2)
        },
        {
            "holding_id": "hld_006",
            "user_id": "usr_001",
            "account_id": "acc_001",
            "ticker": "GLD",
            "asset_class": "COMMODITY",
            "quantity": 65.0,
            "average_cost": 205.00,
            "current_price": 224.50,
            "market_value": round(65.0 * 224.50, 2)
        },
        {
            "holding_id": "hld_007",
            "user_id": "usr_001",
            "account_id": "acc_001",
            "ticker": "BIL",
            "asset_class": "CASH_EQUIVALENT",
            "quantity": 310.0,
            "average_cost": 91.50,
            "current_price": 91.65,
            "market_value": round(310.0 * 91.65, 2)
        }
    ]

    holdings_file = os.path.join(output_dir, "holdings.csv")
    with open(holdings_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(holdings[0].keys()))
        writer.writeheader()
        writer.writerows(holdings)

    # 5. TRANSACTIONS (180 days of realistic financial transactions with categories and anomalies)
    categories = [
        ("INCOME_SALARY", "Direct Deposit - Tech Global Inc", 8500.00, "CREDIT", True),
        ("HOUSING", "Highline Luxury Living Rent", 3200.00, "DEBIT", True),
        ("INVESTMENT", "Automated Brokerage Deposit", 2500.00, "DEBIT", True),
        ("FOOD_GROCERIES", "Whole Foods Market", 165.40, "DEBIT", False),
        ("FOOD_DINING", "Nobu Downtown", 245.80, "DEBIT", False),
        ("FOOD_DINING", "Blue Bottle Coffee", 8.50, "DEBIT", False),
        ("UTILITIES", "ConEdison Electric", 145.20, "DEBIT", True),
        ("SUBSCRIPTION", "Bloomberg Terminal / AWS Cloud", 340.00, "DEBIT", True),
        ("TRANSPORT", "Uber Black", 42.50, "DEBIT", False),
        ("HEALTH", "Equinox Fitness", 295.00, "DEBIT", True),
        ("TRAVEL", "Delta Air Lines", 680.00, "DEBIT", False)
    ]

    transactions = []
    start_date = datetime(2026, 4, 1)
    tx_counter = 1000

    # Recurring monthly payments for 6 months
    for month_offset in range(6):
        cur_month_date = start_date + timedelta(days=month_offset * 30)
        # Salary on 1st and 15th
        for day in [1, 15]:
            tx_counter += 1
            transactions.append({
                "transaction_id": f"tx_{tx_counter}",
                "user_id": "usr_001",
                "account_id": "acc_001",
                "date": (cur_month_date.replace(day=day)).strftime("%Y-%m-%d"),
                "merchant": "Tech Global Inc - Payroll",
                "category": "INCOME",
                "amount": 8750.00,
                "type": "CREDIT",
                "is_recurring": 1
            })

        # Rent on 1st
        tx_counter += 1
        transactions.append({
            "transaction_id": f"tx_{tx_counter}",
            "user_id": "usr_001",
            "account_id": "acc_001",
            "date": (cur_month_date.replace(day=1)).strftime("%Y-%m-%d"),
            "merchant": "Highline Luxury Living",
            "category": "HOUSING",
            "amount": 3200.00,
            "type": "DEBIT",
            "is_recurring": 1
        })

        # Random lifestyle transactions
        for _ in range(12):
            tx_counter += 1
            cat, merch, base_amt, tx_type, is_rec = random.choice(categories[3:])
            # add small random variation +/- 15%
            jitter = random.uniform(0.85, 1.15)
            amt = round(base_amt * jitter, 2)
            day = random.randint(2, 28)
            transactions.append({
                "transaction_id": f"tx_{tx_counter}",
                "user_id": "usr_001",
                "account_id": "acc_001",
                "date": (cur_month_date.replace(day=day)).strftime("%Y-%m-%d"),
                "merchant": merch,
                "category": cat,
                "amount": amt,
                "type": tx_type,
                "is_recurring": 1 if is_rec else 0
            })

    # Add 2 intentional anomalies for ML anomaly detector validation
    tx_counter += 1
    transactions.append({
        "transaction_id": f"tx_{tx_counter}",
        "user_id": "usr_001",
        "account_id": "acc_001",
        "date": "2026-08-14",
        "merchant": "Rolex Boutique Fifth Ave",
        "category": "LUXURY_PURCHASE",
        "amount": 14200.00,
        "type": "DEBIT",
        "is_recurring": 0
    })

    tx_counter += 1
    transactions.append({
        "transaction_id": f"tx_{tx_counter}",
        "user_id": "usr_001",
        "account_id": "acc_001",
        "date": "2026-09-02",
        "merchant": "Private Jet Charter Global",
        "category": "TRAVEL",
        "amount": 9850.00,
        "type": "DEBIT",
        "is_recurring": 0
    })

    # Sort transactions by date
    transactions.sort(key=lambda x: x["date"])

    transactions_file = os.path.join(output_dir, "transactions.csv")
    with open(transactions_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(transactions[0].keys()))
        writer.writeheader()
        writer.writerows(transactions)

    # 6. HISTORICAL PRICES (252 trading days for each ticker)
    prices = []
    base_dates = [start_date + timedelta(days=i) for i in range(180)]
    trading_dates = [d for d in base_dates if d.weekday() < 5] # Weekdays only

    for asset in assets:
        t = asset["ticker"]
        price = asset["base_price"]
        annual_vol = asset["annual_volatility"]
        daily_vol = annual_vol / math.sqrt(252)

        for d in trading_dates:
            daily_shock = random.gauss(0.0004, daily_vol) # slight positive upward drift
            price = round(price * (1 + daily_shock), 2)
            prices.append({
                "ticker": t,
                "date": d.strftime("%Y-%m-%d"),
                "close_price": price,
                "daily_return": round(daily_shock, 5)
            })

    prices_file = os.path.join(output_dir, "prices.csv")
    with open(prices_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(prices[0].keys()))
        writer.writeheader()
        writer.writerows(prices)

    print(f"Data generation complete. Datasets written to: {output_dir}")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "data/sample"
    generate_financial_data(target)
