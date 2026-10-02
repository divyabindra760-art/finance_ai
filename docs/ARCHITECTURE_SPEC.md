# LegacyAI — Architecture Specification & Implementation Plan

## 1. Current Architecture
* **Frontend Paradigm**: Single-page application (SPA) built with React 19, TypeScript, and Vite 8.
* **Styling**: Tailwind CSS (v3.4.19) extended with an Editorial Neo-Brutalism design system (high-contrast `#08090C` black, paper white, electric cobalt blue `#0052FF`, monospace coordinates, sharp borders, and tactile drop shadows `shadow-brutal`).
* **Audio Synthesis Engine**: Client-side zero-dependency Web Audio API synthesizer for tactile clicks and harmonic feedback chords.
* **Current Execution Model**: 100% client-side presentation prototype. No server or persistent state.

---

## 2. Current Components
* `Navbar.tsx`: Sticky navigation with protocol ticker telemetry, section anchor jumps, audio mute switch, and mobile menu drawer.
* `Hero.tsx`: High-impact editorial headline with brutalist action buttons.
* `HeroVisual.tsx`: Interactive SVG asset trajectory chart with point inspection tooltips and dynamic simulation spinner.
* `Mission.tsx`: Editorial manifesto with 4 core philosophy principles.
* `Solutions.tsx`: 4-pillar solution cards with expandable detail drawers.
* `AIIntelligence.tsx`: Interactive quant node interface with multi-timeframe SVG trajectory redrawing, simulated rebalancing action, risk stress test tab, and decision log viewer.
* `HowItWorks.tsx`: 3-step timeline (Connect Accounts → AI Analysis → Autonomous Execution).
* `Security.tsx`: Zero-trust security, encryption (AES-256-GCM), and regulatory compliance matrix.
* `GetStartedModal.tsx`: Dual-mode modal for capital/strategy onboarding and instant portfolio simulation.
* `CTA.tsx`: Conversion callout banner.
* `Footer.tsx`: Institutional footer with regulatory disclosures (FINRA/SIPC alignment) and newsletter signup.

---

## 3. Current Data Flow
* **State Management**: Local component state (`useState`, `useEffect`) in `App.tsx` and individual components.
* **Component Communication**: Callbacks passed via props (e.g. `onOpenGetStarted`, `onToggleSound`).
* **Data Sources**: Hardcoded constants and static objects embedded directly inside React component files.

---

## 4. Current Mocked Features
* **Portfolio Metrics**: The `$284,620` portfolio value, 8.42% 1-month return, and asset allocation percentages are hardcoded.
* **Chart Vectors**: SVG paths are pre-calculated strings (`M 0 150 Q 90 140...`).
* **Rebalancing Execution**: Toggling a Boolean state (`actionApplied`) with a 600ms timer and chime.
* **Onboarding & Waitlist**: Simulates a 1200ms loading delay before showing completion without storing emails or inputs.
* **Decision Trace & Stress Tests**: Static text logs without live calculation or database storage.

---

## 5. Current Dependencies
* **Frontend**: `react` (^19.2.8), `react-dom` (^19.2.8), `lucide-react` (^1.43.0), `tailwindcss` (^3.4.19), `typescript` (~6.0.2), `vite` (^8.2.2).
* **Remote Repository Context**: The upstream repository (`divyabindra760-art/finance_ai`) contains an earlier Python prototype with `langchain`, `chromadb`, `alpha_vantage`, and `gradio`.

---

## 6. Proposed Backend Architecture (FastAPI + Python)
```
                    LEGACYAI
                       │
                React + TypeScript
                       │
                       ▼
                 FastAPI Backend
                       │
                AI Orchestrator
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
    RAG Engine      Data Tools       ML Engine
  (Chroma/Qdrant)  (Pandas/NumPy)  (Scikit-Learn/TF)
       │               │                │
       └───────────────┼────────────────┘
                       ▼
             PostgreSQL + SQLAlchemy
                       │
                       ▼
                 Decision Logs
```

* **Core Framework**: FastAPI with Pydantic v2 validation models and async request handling.
* **Calculation Engine**: Strict isolation — financial math and analytics run exclusively in Python with NumPy and Pandas, never inside React components.
* **Security**: CORS middleware, environment configuration via `.env`, and secret keys stored strictly on the server.

---

## 7. Proposed Database Schema (PostgreSQL + SQLAlchemy)
* `users`: `id`, `email`, `hashed_password`, `full_name`, `created_at`, `risk_profile`.
* `accounts`: `id`, `user_id`, `name`, `type` (checking, brokerage, crypto, savings), `balance`, `currency`.
* `holdings`: `id`, `user_id`, `account_id`, `ticker`, `asset_class`, `quantity`, `avg_cost`, `current_price`, `updated_at`.
* `transactions`: `id`, `user_id`, `account_id`, `date`, `merchant`, `category`, `amount`, `type` (debit, credit, transfer).
* `portfolio_snapshots`: `id`, `user_id`, `timestamp`, `total_value`, `cash_value`, `equity_value`, `fixed_income_value`, `real_assets_value`.
* `market_prices`: `id`, `ticker`, `timestamp`, `price`, `volume`, `change_pct`.
* `documents`: `id`, `title`, `source`, `publication_date`, `file_path`, `checksum`.
* `document_chunks`: `id`, `document_id`, `chunk_index`, `content`, `page_number`, `section_title`, `embedding_id`.
* `chat_sessions`: `id`, `user_id`, `created_at`, `title`.
* `chat_messages`: `id`, `session_id`, `sender` (user, agent), `content`, `metadata_json`, `timestamp`.
* `decision_logs`: `id`, `user_id`, `message_id`, `intent`, `tools_called_json`, `calculations_json`, `sources_cited_json`, `model_confidence`, `execution_time_ms`, `timestamp`.

---

## 8. Proposed AI Agent Architecture
```
User Message
    │
    ▼
FastAPI (/api/chat)
    │
    ▼
AI Orchestrator (Intent Detection & Planner)
    │
    ├─► If Portfolio/Risk: Call `analyze_portfolio(user_id)` (SQL + Pandas/NumPy)
    ├─► If Spending/Cash Flow: Call `analyze_transactions(user_id)` (Pandas)
    ├─► If Macro/Scenario: Call `simulate_inflation()` or `stress_test_portfolio()` (NumPy)
    ├─► If Market Price: Call `get_market_price(ticker)` (Alpha Vantage/Finnhub/Mock)
    ├─► If Financial Theory/Docs: Call `search_financial_documents(query)` (RAG)
    │
    ▼
Structured Tool Aggregation & Analysis
    │
    ▼
LLM Reasoning & Plain-English Explanation
    │
    ▼
Structured Response Payload (Answer + Charts Data + Tables + Sources + Audit Trace)
    │
    ▼
Record to PostgreSQL `decision_logs`
```

---

## 9. Proposed RAG Architecture
* **Ingestion Pipeline**: Ingestion of verified financial education and research documents (FED reports, SEC 10-K disclosures, portfolio theory papers).
* **Chunking**: Recursive character text splitting (500–800 tokens) with 100-token sliding window overlap.
* **Metadata Schema**: Preserves `document_id`, `title`, `source`, `page_number`, `section`, and `chunk_id`.
* **Vector Store**: ChromaDB / Qdrant with standardized cosine similarity retrieval.
* **Retrieval & Citation**: Grounded context injection with strict instructions to cite source, page, and section.

---

## 10. Proposed ML Architecture
* **Task 1: Cash Flow Anomaly Detection**:
  * Input features: Transaction amount, merchant category frequency, day-of-month, distance from category rolling mean.
  * Model: Isolation Forest and rolling Z-score statistical baseline for anomaly flagging.
* **Task 2: Portfolio Volatility & Risk Forecasting**:
  * Time-series variance modeling for risk regime detection.
  * Separation of concerns: Analytics (Pandas/NumPy) calculates descriptive statistics, ML models identify anomalies/predictions, and LLM provides human-readable explanations.

---

## 11. Files That Will Be Created & Modified

### Backend Structure to be Created:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── health.py
│   │       ├── chat.py
│   │       ├── portfolio.py
│   │       ├── transactions.py
│   │       ├── market.py
│   │       ├── scenarios.py
│   │       └── decisions.py
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── tools.py
│   │   └── prompts.py
│   ├── data/
│   │   ├── generator.py
│   │   ├── loaders.py
│   │   ├── analytics.py
│   │   └── scenarios.py
│   ├── db/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── embeddings.py
│   │   └── retriever.py
│   └── ml/
│       ├── features.py
│       └── anomaly_detector.py
├── data/
│   ├── sample/
│   │   ├── users.csv
│   │   ├── accounts.csv
│   │   ├── holdings.csv
│   │   ├── transactions.csv
│   │   └── prices.csv
│   └── documents/
│       └── financial_handbook.txt
├── tests/
│   ├── test_analytics.py
│   ├── test_scenarios.py
│   └── test_api.py
├── requirements.txt
└── .env.example
```

### Frontend Files to be Modified / Created:
* Create `src/services/api.ts` (Typed API client for backend communication).
* Create `src/components/AdvisoryChatDrawer.tsx` (Interactive AI Advisory interface).
* Create `src/pages/Dashboard.tsx` (Dedicated analytics dashboard).
* Update `src/App.tsx` and `src/components/AIIntelligence.tsx` to consume live backend data.

---

## 12. Phased Milestone Execution Plan

* **MILESTONE 1**: Data Engineering Foundation (Realistic synthetic financial datasets, Pandas loader, NumPy analytics engine, mathematical portfolio & scenario calculators, and unit tests).
* **MILESTONE 2**: Relational Database Layer (SQLAlchemy ORM models, SQLite/PostgreSQL setup, and seed script).
* **MILESTONE 3**: FastAPI REST Backend (Core API routes, Pydantic schemas, CORS, and health checks).
* **MILESTONE 4**: Financial Calculation & Scenario REST APIs (Exposing portfolio, transaction, and inflation calculators via HTTP).
* **MILESTONE 5**: AI Agent Orchestrator & Tool Calling (Structured multi-tool execution and reasoning pipeline).
* **MILESTONE 6**: Grounded RAG Pipeline (Document chunking, vector storage, context injection, and verified citations).
* **MILESTONE 7**: Machine Learning Layer (Isolation Forest anomaly detection on spending and cash flows).
* **MILESTONE 8**: Decision Log Persistence & Audit API (Structured decision traces recorded to database).
* **MILESTONE 9**: Frontend Integration (React API service, Advisory Chat Drawer with structured outputs, and live AI Cockpit).
* **MILESTONE 10**: Client Dashboard Portal, Docker Compose, and Production Verification.
