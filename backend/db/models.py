"""
LegacyAI SQLAlchemy Relational ORM Models
Defines institutional relational schemas with constraints, foreign keys, and indexes for high-throughput querying.
"""

from datetime import datetime
from sqlalchemy import (
    Column, 
    String, 
    Float, 
    Integer, 
    DateTime, 
    ForeignKey, 
    Text, 
    Boolean,
    Index
)
from sqlalchemy.orm import relationship
from backend.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    risk_profile = Column(String(50), default="MODERATE")
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    holdings = relationship("Holding", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    decision_logs = relationship("DecisionLog", back_populates="user", cascade="all, delete-orphan")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False) # TAXABLE_BROKERAGE, HIGH_YIELD_SAVINGS, BUSINESS_CHECKING
    currency = Column(String(10), default="USD")
    cash_balance = Column(Float, default=0.0)

    user = relationship("User", back_populates="accounts")
    holdings = relationship("Holding", back_populates="account", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

class Asset(Base):
    __tablename__ = "assets"

    ticker = Column(String(20), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    asset_class = Column(String(50), nullable=False, index=True) # EQUITY, FIXED_INCOME, REAL_ESTATE, COMMODITY, CASH_EQUIVALENT
    expense_ratio = Column(Float, default=0.0)
    base_price = Column(Float, nullable=False)
    annual_volatility = Column(Float, default=0.15)

    market_prices = relationship("MarketPrice", back_populates="asset", cascade="all, delete-orphan")

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False, index=True)
    account_id = Column(String(50), ForeignKey("accounts.id"), nullable=False, index=True)
    ticker = Column(String(20), ForeignKey("assets.ticker"), nullable=False, index=True)
    asset_class = Column(String(50), nullable=False)
    quantity = Column(Float, nullable=False)
    average_cost = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    market_value = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="holdings")
    account = relationship("Account", back_populates="holdings")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False, index=True)
    account_id = Column(String(50), ForeignKey("accounts.id"), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    merchant = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String(20), nullable=False) # DEBIT, CREDIT
    is_recurring = Column(Boolean, default=False)

    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")

    __table_args__ = (
        Index("idx_tx_user_date", "user_id", "date"),
        Index("idx_tx_user_category", "user_id", "category"),
    )

class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20), ForeignKey("assets.ticker"), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    close_price = Column(Float, nullable=False)
    daily_return = Column(Float, default=0.0)

    asset = relationship("Asset", back_populates="market_prices")

    __table_args__ = (
        Index("idx_price_ticker_date", "ticker", "date"),
    )

class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    total_value = Column(Float, nullable=False)
    invested_value = Column(Float, nullable=False)
    cash_balance = Column(Float, default=0.0)
    hhi_concentration = Column(Float, default=0.0)
    equity_pct = Column(Float, default=0.0)
    fixed_income_pct = Column(Float, default=0.0)
    cash_pct = Column(Float, default=0.0)

class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    query = Column(Text, nullable=False)
    intent = Column(String(100), nullable=False)
    tools_called = Column(Text, nullable=True) # JSON string of executed tools
    calculations = Column(Text, nullable=True) # JSON string of deterministic calculations
    sources_cited = Column(Text, nullable=True) # JSON string of RAG sources
    model_confidence = Column(Float, default=1.0)
    execution_time_ms = Column(Float, default=0.0)

    user = relationship("User", back_populates="decision_logs")
