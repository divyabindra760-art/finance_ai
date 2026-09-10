"""
Financial Document Retrieval Tool
Provides access to the RAG knowledge base for financial document queries.
This tool wraps the existing Milestone 2 RAG pipeline without rebuilding it.
"""

import os
from typing import List, Dict, Any, Optional
from langchain.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Import configuration from existing RAG pipeline
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag_pipeline import CHROMA_PERSIST_DIR, EMBEDDING_MODEL, RETRIEVER_K


class FinancialDocumentRetriever:
    """
    Retrieves information from financial documents using the existing RAG pipeline.
    Reuses the ChromaDB vector store created in Milestone 2.
    """
    
    def __init__(self, persist_directory: str = CHROMA_PERSIST_DIR):
        """
        Initialize the retriever by loading the existing vector store.
        
        Args:
            persist_directory: Path to persisted ChromaDB
        """
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.retriever = None
        self._initialize()
    
    def _initialize(self):
        """Load the existing vector store and create retriever."""
        if not os.path.exists(self.persist_directory):
            raise ValueError(
                f"ChromaDB not found at {self.persist_directory}. "
                "Please run rag_pipeline.py first to create the vector store."
            )
        
        # Initialize embeddings (same model as Milestone 2)
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Load existing vector store from disk
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings
        )
        
        # Create retriever with k=3 (as per Milestone 2)
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": RETRIEVER_K}
        )
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search financial documents for relevant information.
        
        Args:
            query: User's question or search query
        
        Returns:
            List of dictionaries containing:
                - content: The text content
                - source: Source information (page number, document)
                - metadata: Additional metadata
        """
        if not self.retriever:
            raise ValueError("Retriever not initialized")
        
        # Retrieve relevant documents
        docs = self.retriever.invoke(query)
        
        # Format results with metadata
        results = []
        for doc in docs:
            result = {
                "content": doc.page_content,
                "source": f"Page {doc.metadata.get('page', 'N/A')}",
                "metadata": doc.metadata
            }
            results.append(result)
        
        return results
    
    def format_results_for_agent(self, results: List[Dict[str, Any]]) -> str:
        """
        Format retrieval results in a way that's easy for the agent to use.
        
        Args:
            results: List of search results
        
        Returns:
            Formatted string with sources and content
        """
        if not results:
            return "No relevant information found in financial documents."
        
        formatted = []
        formatted.append(f"Found {len(results)} relevant sections from financial documents:\n")
        
        for i, result in enumerate(results, 1):
            formatted.append(f"--- Document Section {i} ---")
            formatted.append(f"Source: {result['source']}")
            formatted.append(f"Content: {result['content'][:500]}...")  # Truncate long content
            formatted.append("")
        
        return "\n".join(formatted)


# Global retriever instance (initialized once)
_retriever_instance = None


def get_financial_document_retriever() -> FinancialDocumentRetriever:
    """
    Get or create the global retriever instance.
    Singleton pattern to avoid reloading the vector store multiple times.
    """
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = FinancialDocumentRetriever()
    return _retriever_instance


@tool
def search_financial_documents(query: str) -> str:
    """
    Search and retrieve information from uploaded financial documents (e.g., annual reports, 10-K filings, fund fact sheets).
    
    This tool searches through the vector database containing embedded financial documents and returns relevant sections
    that match the query. Use this tool when the user asks questions about:
    
    WHEN TO USE THIS TOOL:
    - Company financial statements (revenue, expenses, net income, cash flow)
    - Historical financial performance from annual reports
    - Risk factors mentioned in financial filings
    - Company operations, products, or business segments described in documents
    - Management commentary or forward guidance from reports
    - Any information that would be in a financial document (10-K, annual report, etc.)
    - Questions asking "according to the report/document/filing"
    
    EXAMPLES OF QUERIES FOR THIS TOOL:
    - "What was Apple's revenue last year according to the 10-K?"
    - "What risks did the company mention in their annual report?"
    - "What does the report say about operating expenses?"
    - "According to the filing, what are the company's main product lines?"
    - "What forward guidance did management provide?"
    
    WHEN NOT TO USE THIS TOOL:
    - Current/live stock prices (use live stock price tool instead)
    - Real-time market data (use appropriate market data tool)
    - Historical stock price movements (use historical market data tool)
    - Company fundamentals not in documents (use company fundamentals tool)
    - Recent news or events (use news/sentiment tool)
    
    INPUT:
    - query (str): The user's question or search query. Be specific and include key terms.
    
    OUTPUT:
    Returns a formatted string containing:
    - Number of relevant sections found
    - Content from each section (with source page numbers)
    - Clearly labeled as "STATIC/HISTORICAL" data from financial documents
    
    IMPORTANT NOTES:
    - This tool returns STATIC/HISTORICAL information from documents, not live data
    - Results include source page numbers for citation
    - If no relevant information is found, the tool will explicitly state that
    - The tool searches through 365 pre-indexed document chunks
    - Returns the top 3 most relevant sections
    
    Args:
        query: The search query or question about financial documents
    
    Returns:
        Formatted string with retrieved information and sources
    """
    try:
        retriever = get_financial_document_retriever()
        results = retriever.search(query)
        
        if not results:
            return (
                "No relevant information found in the financial documents for this query. "
                "The uploaded documents may not contain information about this topic."
            )
        
        # Format results with clear labeling
        formatted = ["=" * 60]
        formatted.append("📄 FINANCIAL DOCUMENT RETRIEVAL RESULTS (STATIC/HISTORICAL)")
        formatted.append("=" * 60)
        formatted.append(f"\nQuery: {query}")
        formatted.append(f"Found {len(results)} relevant sections:\n")
        
        for i, result in enumerate(results, 1):
            formatted.append(f"--- Section {i} ---")
            formatted.append(f"📍 Source: {result['source']}")
            formatted.append(f"📝 Content:")
            # Truncate very long content but keep enough context
            content = result['content']
            if len(content) > 800:
                content = content[:800] + "... [truncated]"
            formatted.append(content)
            formatted.append("")
        
        formatted.append("=" * 60)
        formatted.append("Note: This information is from uploaded financial documents (STATIC/HISTORICAL data).")
        formatted.append("=" * 60)
        
        return "\n".join(formatted)
        
    except ValueError as e:
        return (
            f"❌ Error accessing financial documents: {str(e)}\n\n"
            "Please ensure the RAG pipeline has been initialized. "
            "Run 'python rag_pipeline.py' to set up the document knowledge base."
        )
    except Exception as e:
        return (
            f"❌ Unexpected error during document search: {str(e)}\n\n"
            "Please contact support if this issue persists."
        )


# Export the tool for use in agents
__all__ = ['search_financial_documents', 'FinancialDocumentRetriever', 'get_financial_document_retriever']
