"""
LegacyAI Financial Intelligence Platform — FastAPI Application
Production-grade REST API powering autonomous financial analytics, portfolio risk stress testing, and auditable decision logs.
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db.database import init_db
from backend.db.seed import seed_database
from backend.api.routes.health import router as health_router
from backend.api.routes.portfolio import router as portfolio_router
from backend.api.routes.transactions import router as transactions_router
from backend.api.routes.scenarios import router as scenarios_router
from backend.api.routes.decisions import router as decisions_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables and sample seeds are ready
    try:
        init_db()
        seed_database()
    except Exception as e:
        print(f"Startup database check: {e}")
    yield
    # Shutdown logic if needed

app = FastAPI(
    title="LegacyAI Financial Intelligence API",
    description="Algorithmic financial copilot API providing quantitative portfolio risk analytics, cash flow velocity, and scenario simulation.",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS for local development and frontend client connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(health_router)
app.include_router(portfolio_router)
app.include_router(transactions_router)
app.include_router(scenarios_router)
app.include_router(decisions_router)

@app.get("/")
def root():
    return {
        "service": "LegacyAI Financial Intelligence API",
        "version": "2.0.0",
        "docs_url": "/docs",
        "health_check": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
