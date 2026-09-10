# InvestIQ - Personal Investment Research Agent

A hackathon project that answers questions against financial documents and pulls live market data.

## Project Status

### Milestone 1: Basic Setup ✓
- Project structure created
- ChatOllama connection test

### Milestone 2: RAG Pipeline ✓ COMPLETE
- Financial PDF document loaded (80-page Apple 10-K)
- Document split into 365 chunks
- HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)
- ChromaDB vector store with persistence
- Retriever configured (k=3)
- Retrieval tests passed for revenue, net income, and cash flow queries

### Milestone 3: Agent & Tools ✅ COMPLETE
- ✅ Directory structure created (`tools/`, `services/`, `agent/`, `tests/`)
- ✅ Dependencies installed (langchain, langgraph, requests, pytest)
- ✅ Alpha Vantage service with comprehensive error handling
- ✅ Five tools implemented with detailed agent-facing descriptions:
  1. ✅ Financial document retrieval tool (reuses Milestone 2 RAG)
  2. ✅ Live stock price tool (Alpha Vantage)
  3. ✅ Historical market data tool (Alpha Vantage)
  4. ✅ Company fundamentals tool (Alpha Vantage)
  5. ✅ Financial news/sentiment tool (Alpha Vantage)
- ✅ Investment research agent (LangGraph + ChatOllama with Qwen 2.5 7B)
- ✅ Comprehensive test suite (51 tests passing)
- ✅ Clear STATIC/HISTORICAL vs LIVE data labeling
- ✅ Graceful error handling throughout

### Milestone 4: Gradio UI ✅ COMPLETE
- ✅ Gradio interface (`app.py`) wrapping existing agent
- ✅ Clean chatbot UI with disclaimer
- ✅ Example questions for easy testing
- ✅ Error handling for Ollama/API failures
- ✅ Clear data source labeling in responses
- ✅ No breaking changes to Milestones 1-3

### Milestone 4: UI (Not Started)
- Streamlit interface
- Disclaimer display

## Setup

1. Install dependencies (start with essentials):
```bash
pip install langchain-ollama
```

Or install all at once (may take several minutes):
```bash
pip install -r requirements.txt
```

2. Ensure Ollama is running locally with a model (e.g., qwen3:0.6b)
   - Check available models: `ollama list`
   - Pull a new model if needed: `ollama pull llama3.2`

3. Test ChatOllama connection:
```bash
python test_ollama.py
```

## Current Status - Milestone 1 ✓ COMPLETE

### What We Checked:
1. ✓ Python 3.13.5 is installed and working
2. ✓ Ollama 0.33.3 is installed and running
3. ✓ Model `qwen3:0.6b` is available
4. ✓ `langchain-ollama` package installed successfully
5. ✓ ChatOllama connection test passed

### What Was Created:
- `requirements.txt` - All project dependencies
- `test_ollama.py` - Basic ChatOllama connectivity test (PASSED ✓)
- `README.md` - Project documentation
- `.gitignore` - Git ignore rules

### Test Result:
```
InvestIQ - Milestone 1: ChatOllama Connection Test
✓ ChatOllama initialized successfully
✓ ChatOllama is working correctly!
Response: "2 plus 2 equals 4."
```
