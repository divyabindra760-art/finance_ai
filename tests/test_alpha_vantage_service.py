"""
Tests for Alpha Vantage Service
Tests use mocked responses to avoid real API calls.
"""

import os
import pytest
import requests
from unittest.mock import patch, Mock
from services.alpha_vantage_service import (
    AlphaVantageService,
    AlphaVantageError,
    APIKeyMissingError,
    InvalidSymbolError,
    RateLimitError,
    APIResponseError,
    get_alpha_vantage_service
)


# Mock responses for testing
MOCK_QUOTE_RESPONSE = {
    "Global Quote": {
        "01. symbol": "AAPL",
        "05. price": "150.25",
        "09. change": "2.50",
        "10. change percent": "1.69%",
        "06. volume": "50000000",
        "07. latest trading day": "2025-01-10"
    }
}

MOCK_TIME_SERIES_RESPONSE = {
    "Meta Data": {
        "1. Information": "Daily Prices",
        "2. Symbol": "AAPL"
    },
    "Time Series (Daily)": {
        "2025-01-10": {
            "1. open": "148.00",
            "2. high": "151.00",
            "3. low": "147.50",
            "4. close": "150.25",
            "5. volume": "50000000"
        }
    }
}

MOCK_OVERVIEW_RESPONSE = {
    "Symbol": "AAPL",
    "Name": "Apple Inc",
    "Description": "Apple Inc. designs and manufactures technology products.",
    "Sector": "Technology",
    "MarketCapitalization": "2500000000000",
    "PERatio": "28.5",
    "EPS": "5.25",
    "DividendYield": "0.0062",
    "RevenueTTM": "394000000000"
}

MOCK_NEWS_RESPONSE = {
    "feed": [
        {
            "title": "Apple announces new product",
            "summary": "Apple unveiled new products today.",
            "overall_sentiment_score": 0.35,
            "overall_sentiment_label": "Bullish"
        }
    ],
    "sentiment_score_definition": "x <= -0.35: Bearish; -0.35 < x <= -0.15: Somewhat-Bearish"
}


class TestAlphaVantageService:
    """Test suite for AlphaVantageService"""
    
    def test_init_with_api_key(self):
        """Test service initialization with explicit API key"""
        service = AlphaVantageService(api_key="test_key_123")
        assert service.api_key == "test_key_123"
    
    def test_init_without_api_key_raises_error(self):
        """Test that missing API key raises appropriate error"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(APIKeyMissingError) as exc_info:
                AlphaVantageService()
            assert "API key not found" in str(exc_info.value)
    
    def test_init_with_env_variable(self):
        """Test service initialization from environment variable"""
        with patch.dict('os.environ', {'ALPHA_VANTAGE_API_KEY': 'env_key_456'}):
            service = AlphaVantageService()
            assert service.api_key == "env_key_456"
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_get_quote_success(self, mock_get):
        """Test successful quote retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = MOCK_QUOTE_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="test_key")
        result = service.get_quote("AAPL")
        
        assert result["symbol"] == "AAPL"
        assert result["price"] == 150.25
        assert result["change"] == 2.50
        assert result["change_percent"] == "1.69"
        assert result["volume"] == 50000000
        assert result["latest_trading_day"] == "2025-01-10"
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_get_quote_invalid_symbol(self, mock_get):
        """Test quote retrieval with invalid symbol"""
        mock_response = Mock()
        mock_response.json.return_value = {"Global Quote": {}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="test_key")
        
        with pytest.raises(InvalidSymbolError) as exc_info:
            service.get_quote("INVALID123")
        assert "No data found" in str(exc_info.value)
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_get_quote_api_error_message(self, mock_get):
        """Test handling of API error message"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Error Message": "Invalid API call. Please check documentation."
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="test_key")
        
        with pytest.raises(InvalidSymbolError):
            service.get_quote("XYZ")
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_rate_limit_error(self, mock_get):
        """Test handling of rate limit"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute."
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="test_key")
        
        with pytest.raises(RateLimitError) as exc_info:
            service.get_quote("AAPL")
        assert "rate limit" in str(exc_info.value).lower()
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_network_timeout(self, mock_get):
        """Test handling of network timeout"""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        service = AlphaVantageService(api_key="test_key")
        
        with pytest.raises(APIResponseError) as exc_info:
            service.get_quote("AAPL")
        assert "timed out" in str(exc_info.value).lower()
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_get_time_series_success(self, mock_get):
        """Test successful time series retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = MOCK_TIME_SERIES_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="test_key")
        result = service.get_time_series_daily("AAPL")
        
        assert result["symbol"] == "AAPL"
        assert "time_series" in result
        assert "2025-01-10" in result["time_series"]
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_get_company_overview_success(self, mock_get):
        """Test successful company overview retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = MOCK_OVERVIEW_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="test_key")
        result = service.get_company_overview("AAPL")
        
        assert result["Symbol"] == "AAPL"
        assert result["Name"] == "Apple Inc"
        assert result["Sector"] == "Technology"
        assert "MarketCapitalization" in result
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_get_company_overview_invalid_symbol(self, mock_get):
        """Test company overview with invalid symbol"""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="test_key")
        
        with pytest.raises(InvalidSymbolError):
            service.get_company_overview("INVALID")
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_get_news_sentiment_success(self, mock_get):
        """Test successful news sentiment retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = MOCK_NEWS_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="test_key")
        result = service.get_news_sentiment(tickers="AAPL")
        
        assert "feed" in result
        assert len(result["feed"]) > 0
        assert "overall_sentiment_score" in result["feed"][0]
    
    def test_empty_symbol_validation(self):
        """Test that empty symbol is rejected"""
        service = AlphaVantageService(api_key="test_key")
        
        with pytest.raises(InvalidSymbolError):
            service.get_quote("")
        
        with pytest.raises(InvalidSymbolError):
            service.get_quote(None)
    
    def test_symbol_normalization(self):
        """Test that symbols are normalized (uppercase, stripped)"""
        service = AlphaVantageService(api_key="test_key")
        
        with patch.object(service, '_make_request') as mock_request:
            mock_request.return_value = MOCK_QUOTE_RESPONSE
            
            # Should normalize lowercase and whitespace
            service.get_quote("  aapl  ")
            
            # Check that the request was made with normalized symbol
            call_args = mock_request.call_args
            assert call_args[0][1]["symbol"] == "AAPL"
    
    def test_factory_function(self):
        """Test the factory function"""
        service = get_alpha_vantage_service(api_key="test_key")
        assert isinstance(service, AlphaVantageService)
        assert service.api_key == "test_key"
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_health_check_success(self, mock_get):
        """Test health check with valid API key"""
        mock_response = Mock()
        mock_response.json.return_value = MOCK_QUOTE_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="test_key")
        assert service.health_check() is True
    
    @patch('services.alpha_vantage_service.requests.get')
    def test_health_check_failure(self, mock_get):
        """Test health check with invalid API key"""
        mock_response = Mock()
        mock_response.json.return_value = {"Error Message": "Invalid API key"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AlphaVantageService(api_key="invalid_key")
        assert service.health_check() is False


# Integration-style test (can be skipped if no API key)
class TestAlphaVantageServiceIntegration:
    """
    Integration tests that require a real API key.
    These tests are skipped by default.
    Set ALPHA_VANTAGE_API_KEY environment variable to run them.
    """
    
    @pytest.mark.skipif(
        not os.getenv("ALPHA_VANTAGE_API_KEY"),
        reason="No API key configured"
    )
    def test_real_api_call(self):
        """Test with real API (requires valid key)"""
        service = AlphaVantageService()
        
        # Test with a known symbol
        result = service.get_quote("AAPL")
        
        assert result["symbol"] == "AAPL"
        assert result["price"] > 0
        assert "latest_trading_day" in result


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
