"""
LegacyAI Data Loaders
Institutional Pandas data ingestion for users, accounts, holdings, transactions, and prices.
"""

import os
from typing import Optional
import pandas as pd

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "sample")

def get_data_path(filename: str, data_dir: Optional[str] = None) -> str:
    base = data_dir or DEFAULT_DATA_DIR
    return os.path.join(base, filename)

def load_users(data_dir: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path("users.csv", data_dir)
    df = pd.read_csv(path)
    df["created_at"] = pd.to_datetime(df["created_at"])
    return df

def load_accounts(data_dir: Optional[str] = None, user_id: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path("accounts.csv", data_dir)
    df = pd.read_csv(path)
    if user_id:
        df = df[df["user_id"] == user_id].copy()
    return df

def load_assets(data_dir: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path("assets.csv", data_dir)
    return pd.read_csv(path)

def load_holdings(data_dir: Optional[str] = None, user_id: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path("holdings.csv", data_dir)
    df = pd.read_csv(path)
    if user_id:
        df = df[df["user_id"] == user_id].copy()
    df["unrealized_gain_loss"] = (df["current_price"] - df["average_cost"]) * df["quantity"]
    df["gain_loss_pct"] = ((df["current_price"] - df["average_cost"]) / df["average_cost"]) * 100.0
    return df

def load_transactions(data_dir: Optional[str] = None, user_id: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path("transactions.csv", data_dir)
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    if user_id:
        df = df[df["user_id"] == user_id].copy()
    return df.sort_values(by="date", ascending=True).reset_index(drop=True)

def load_prices(data_dir: Optional[str] = None, ticker: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path("prices.csv", data_dir)
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    if ticker:
        df = df[df["ticker"] == ticker].copy()
    return df.sort_values(by="date", ascending=True).reset_index(drop=True)
