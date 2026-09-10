"""
Tests for Financial Document Retrieval Tool
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from tools.financial_document_tool import (
    FinancialDocumentRetriever,
    search_financial_documents,
    get_financial_document_retriever
)


# Mock document data for testing
MOCK_DOC_1 = Mock()
MOCK_DOC_1.page_content = "Apple Inc. reported total net sales of $416,161 million for fiscal year 2025."
MOCK_DOC_1.metadata = {"page": 31, "source": "apple_10k_2025.pdf"}

MOCK_DOC_2 = Mock()
MOCK_DOC_2.page_content = "Net income for 2025 was $112,010 million, up from $93,736 million in 2024."
MOCK_DOC_2.metadata = {"page": 35, "source": "apple_10k_2025.pdf"}

MOCK_DOC_3 = Mock()
MOCK_DOC_3.page_content = "Operating cash flow increased significantly due to strong product sales."
MOCK_DOC_3.metadata = {"page": 45, "source": "apple_10k_2025.pdf"}


class TestFinancialDocumentRetriever:
    """Test suite for FinancialDocumentRetriever class"""
    
    @patch('tools.financial_document_tool.os.path.exists')
    @patch('tools.financial_document_tool.Chroma')
    @patch('tools.financial_document_tool.HuggingFaceEmbeddings')
    def test_init_success(self, mock_embeddings, mock_chroma, mock_exists):
        """Test successful initialization"""
        mock_exists.return_value = True
        mock_vectorstore = Mock()
        mock_retriever = Mock()
        mock_vectorstore.as_retriever.return_value = mock_retriever
        mock_chroma.return_value = mock_vectorstore
        
        retriever = FinancialDocumentRetriever()
        
        assert retriever.vectorstore is not None
        assert retriever.retriever is not None
        mock_embeddings.assert_called_once()
        mock_chroma.assert_called_once()
    
    @patch('tools.financial_document_tool.os.path.exists')
    def test_init_no_chroma_db(self, mock_exists):
        """Test initialization fails when ChromaDB doesn't exist"""
        mock_exists.return_value = False
        
        with pytest.raises(ValueError) as exc_info:
            FinancialDocumentRetriever()
        
        assert "ChromaDB not found" in str(exc_info.value)
    
    @patch('tools.financial_document_tool.os.path.exists')
    @patch('tools.financial_document_tool.Chroma')
    @patch('tools.financial_document_tool.HuggingFaceEmbeddings')
    def test_search_returns_results(self, mock_embeddings, mock_chroma, mock_exists):
        """Test search returns properly formatted results"""
        mock_exists.return_value = True
        mock_vectorstore = Mock()
        mock_retriever = Mock()
        mock_retriever.invoke.return_value = [MOCK_DOC_1, MOCK_DOC_2]
        mock_vectorstore.as_retriever.return_value = mock_retriever
        mock_chroma.return_value = mock_vectorstore
        
        retriever = FinancialDocumentRetriever()
        results = retriever.search("What was the revenue?")
        
        assert len(results) == 2
        assert results[0]["content"] == MOCK_DOC_1.page_content
        assert results[0]["source"] == "Page 31"
        assert "page" in results[0]["metadata"]
    
    @patch('tools.financial_document_tool.os.path.exists')
    @patch('tools.financial_document_tool.Chroma')
    @patch('tools.financial_document_tool.HuggingFaceEmbeddings')
    def test_search_empty_results(self, mock_embeddings, mock_chroma, mock_exists):
        """Test search with no results"""
        mock_exists.return_value = True
        mock_vectorstore = Mock()
        mock_retriever = Mock()
        mock_retriever.invoke.return_value = []
        mock_vectorstore.as_retriever.return_value = mock_retriever
        mock_chroma.return_value = mock_vectorstore
        
        retriever = FinancialDocumentRetriever()
        results = retriever.search("Something not in documents")
        
        assert len(results) == 0
    
    @patch('tools.financial_document_tool.os.path.exists')
    @patch('tools.financial_document_tool.Chroma')
    @patch('tools.financial_document_tool.HuggingFaceEmbeddings')
    def test_format_results_for_agent(self, mock_embeddings, mock_chroma, mock_exists):
        """Test formatting of results for agent consumption"""
        mock_exists.return_value = True
        mock_vectorstore = Mock()
        mock_vectorstore.as_retriever.return_value = Mock()
        mock_chroma.return_value = mock_vectorstore
        
        retriever = FinancialDocumentRetriever()
        
        results = [
            {
                "content": "Test content",
                "source": "Page 10",
                "metadata": {"page": 10}
            }
        ]
        
        formatted = retriever.format_results_for_agent(results)
        
        assert "Found 1 relevant sections" in formatted
        assert "Page 10" in formatted
        assert "Test content" in formatted
    
    @patch('tools.financial_document_tool.os.path.exists')
    @patch('tools.financial_document_tool.Chroma')
    @patch('tools.financial_document_tool.HuggingFaceEmbeddings')
    def test_format_empty_results(self, mock_embeddings, mock_chroma, mock_exists):
        """Test formatting of empty results"""
        mock_exists.return_value = True
        mock_vectorstore = Mock()
        mock_vectorstore.as_retriever.return_value = Mock()
        mock_chroma.return_value = mock_vectorstore
        
        retriever = FinancialDocumentRetriever()
        formatted = retriever.format_results_for_agent([])
        
        assert "No relevant information found" in formatted


class TestSearchFinancialDocumentsTool:
    """Test suite for the @tool decorated function"""
    
    @patch('tools.financial_document_tool.get_financial_document_retriever')
    def test_tool_success(self, mock_get_retriever):
        """Test successful tool execution"""
        mock_retriever = Mock()
        mock_retriever.search.return_value = [
            {
                "content": "Revenue was $416 billion",
                "source": "Page 31",
                "metadata": {"page": 31}
            }
        ]
        mock_get_retriever.return_value = mock_retriever
        
        result = search_financial_documents.invoke({"query": "What was the revenue?"})
        
        assert "FINANCIAL DOCUMENT RETRIEVAL RESULTS" in result
        assert "STATIC/HISTORICAL" in result
        assert "Revenue was $416 billion" in result
        assert "Page 31" in result
    
    @patch('tools.financial_document_tool.get_financial_document_retriever')
    def test_tool_no_results(self, mock_get_retriever):
        """Test tool with no results found"""
        mock_retriever = Mock()
        mock_retriever.search.return_value = []
        mock_get_retriever.return_value = mock_retriever
        
        result = search_financial_documents.invoke({"query": "Something not in docs"})
        
        assert "No relevant information found" in result
        assert "may not contain information" in result
    
    @patch('tools.financial_document_tool.get_financial_document_retriever')
    def test_tool_value_error(self, mock_get_retriever):
        """Test tool handles ValueError gracefully"""
        mock_get_retriever.side_effect = ValueError("ChromaDB not found")
        
        result = search_financial_documents.invoke({"query": "test query"})
        
        assert "Error accessing financial documents" in result
        assert "ChromaDB not found" in result
    
    @patch('tools.financial_document_tool.get_financial_document_retriever')
    def test_tool_unexpected_error(self, mock_get_retriever):
        """Test tool handles unexpected errors gracefully"""
        mock_retriever = Mock()
        mock_retriever.search.side_effect = Exception("Unexpected error")
        mock_get_retriever.return_value = mock_retriever
        
        result = search_financial_documents.invoke({"query": "test query"})
        
        assert "Unexpected error during document search" in result
    
    @patch('tools.financial_document_tool.get_financial_document_retriever')
    def test_tool_truncates_long_content(self, mock_get_retriever):
        """Test that very long content is truncated"""
        long_content = "A" * 1000
        mock_retriever = Mock()
        mock_retriever.search.return_value = [
            {
                "content": long_content,
                "source": "Page 1",
                "metadata": {"page": 1}
            }
        ]
        mock_get_retriever.return_value = mock_retriever
        
        result = search_financial_documents.invoke({"query": "test"})
        
        assert "[truncated]" in result
        assert len(result) < len(long_content) + 1000  # Much shorter than original
    
    @patch('tools.financial_document_tool.get_financial_document_retriever')
    def test_tool_multiple_results(self, mock_get_retriever):
        """Test tool with multiple document sections"""
        mock_retriever = Mock()
        mock_retriever.search.return_value = [
            {"content": "Section 1 content", "source": "Page 10", "metadata": {}},
            {"content": "Section 2 content", "source": "Page 20", "metadata": {}},
            {"content": "Section 3 content", "source": "Page 30", "metadata": {}}
        ]
        mock_get_retriever.return_value = mock_retriever
        
        result = search_financial_documents.invoke({"query": "test"})
        
        assert "Found 3 relevant sections" in result
        assert "Section 1" in result
        assert "Section 2" in result
        assert "Section 3" in result
        assert "Page 10" in result
        assert "Page 20" in result
        assert "Page 30" in result


class TestToolMetadata:
    """Test the tool's metadata and description"""
    
    def test_tool_has_name(self):
        """Test that tool has a name"""
        assert hasattr(search_financial_documents, 'name')
        assert search_financial_documents.name == 'search_financial_documents'
    
    def test_tool_has_description(self):
        """Test that tool has a description"""
        assert hasattr(search_financial_documents, 'description')
        description = search_financial_documents.description
        
        # Check for key phrases that should be in description
        assert "financial documents" in description.lower()
        assert "when to use" in description.lower()
        assert "when not to use" in description.lower()
    
    def test_tool_description_mentions_examples(self):
        """Test that description includes usage examples"""
        description = search_financial_documents.description
        
        assert "examples" in description.lower()
        assert "revenue" in description.lower() or "10-K" in description or "annual report" in description.lower()
    
    def test_tool_description_mentions_limitations(self):
        """Test that description mentions what NOT to use it for"""
        description = search_financial_documents.description
        
        # Should mention what NOT to use it for
        assert "not" in description.lower()
        assert any(term in description.lower() for term in ["live", "current", "real-time"])


# Integration-style test
@pytest.mark.skipif(
    not os.path.exists("chroma_db"),
    reason="ChromaDB not found - run rag_pipeline.py first"
)
class TestFinancialDocumentToolIntegration:
    """
    Integration test using the real ChromaDB.
    Only runs if ChromaDB exists from Milestone 2.
    """
    
    def test_real_retrieval(self):
        """Test with real ChromaDB (if available)"""
        result = search_financial_documents.invoke({"query": "What was the company's revenue?"})
        
        # Should return formatted results
        assert "FINANCIAL DOCUMENT RETRIEVAL" in result
        assert "Section" in result
        # If ChromaDB exists, it should find something about revenue from Apple 10-K


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
