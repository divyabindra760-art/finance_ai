"""
Tests for Alpha Vantage Tools
Uses mocked API responses to test tool behavior without real API calls.
"""

import pytest
from unittest.mock import patch, Mock
from tools.alpha_vantage_tools import (
    get_live_stock_price,
    get_historical_stock_data,
    get_company_fundamentals,
    get_financial_news_sentiment
)
from services.alpha_vantage_service import (
    InvalidSymbolError,
    RateLimitError,
    APIResponseError
)


class TestLiveStockPriceTool:
    """Tests for get_live_stock_price tool"""
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_successful_quote(self, mock_service):
        """Test successful stock quote retrieval"""
        mock_instance = Mock()
        mock_instance.get_quote.return_value = {
            "symbol": "AAPL",
            "price": 150.25,
            "change": 2.50,
            "change_percent": "1.69",
            "volume": 50000000,
            "latest_trading_day": "2025-01-10"
        }
        mock_service.return_value = mock_instance
        
        result = get_live_stock_price.invoke({"symbol": "AAPL"})
        
        assert "LIVE STOCK QUOTE" in result
        assert "AAPL" in result
        assert "$150.25" in result
        assert "+2.50" in result or "2.50" in result
        assert "50,000,000" in result
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_invalid_symbol(self, mock_service):
        """Test handling of invalid stock symbol"""
        mock_instance = Mock()
        mock_instance.get_quote.side_effect = InvalidSymbolError("Invalid symbol")
        mock_service.return_value = mock_instance
        
        result = get_live_stock_price.invoke({"symbol": "INVALID"})
        
        assert "Invalid stock symbol" in result
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_rate_limit(self, mock_service):
        """Test handling of rate limit error"""
        mock_instance = Mock()
        mock_instance.get_quote.side_effect = RateLimitError("Rate limit exceeded")
        mock_service.return_value = mock_instance
        
        result = get_live_stock_price.invoke({"symbol": "AAPL"})
        
        assert "Rate limit" in result or "rate limit" in result.lower()
    
    def test_tool_has_description(self):
        """Test that tool has comprehensive description"""
        assert hasattr(get_live_stock_price, 'description')
        description = get_live_stock_price.description
        
        # Check for key sections
        assert "when to use" in description.lower()
        assert "when not to use" in description.lower()
        assert "live" in description.lower() or "current" in description.lower()


class TestHistoricalStockDataTool:
    """Tests for get_historical_stock_data tool"""
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_successful_historical_data(self, mock_service):
        """Test successful historical data retrieval"""
        mock_instance = Mock()
        mock_instance.get_time_series_daily.return_value = {
            "symbol": "AAPL",
            "time_series": {
                "2025-01-10": {"4. close": "150.25", "5. volume": "50000000"},
                "2025-01-09": {"4. close": "148.75", "5. volume": "48000000"},
                "2025-01-08": {"4. close": "149.00", "5. volume": "49000000"}
            },
            "meta_data": {}
        }
        mock_service.return_value = mock_instance
        
        result = get_historical_stock_data.invoke({"symbol": "AAPL", "period": "compact"})
        
        assert "HISTORICAL STOCK DATA" in result
        assert "AAPL" in result
        assert "2025-01-10" in result
        assert "$150.25" in result
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_invalid_symbol_historical(self, mock_service):
        """Test handling of invalid symbol for historical data"""
        mock_instance = Mock()
        mock_instance.get_time_series_daily.side_effect = InvalidSymbolError("Invalid symbol")
        mock_service.return_value = mock_instance
        
        result = get_historical_stock_data.invoke({"symbol": "INVALID", "period": "compact"})
        
        assert "Invalid stock symbol" in result
    
    def test_tool_has_description(self):
        """Test that tool has comprehensive description"""
        assert hasattr(get_historical_stock_data, 'description')
        description = get_historical_stock_data.description
        
        assert "historical" in description.lower()
        assert "when to use" in description.lower()
        assert "past" in description.lower() or "performance" in description.lower()


class TestCompanyFundamentalsTool:
    """Tests for get_company_fundamentals tool"""
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_successful_fundamentals(self, mock_service):
        """Test successful fundamentals retrieval"""
        mock_instance = Mock()
        mock_instance.get_company_overview.return_value = {
            "Symbol": "AAPL",
            "Name": "Apple Inc",
            "Sector": "Technology",
            "Industry": "Consumer Electronics",
            "Country": "USA",
            "MarketCapitalization": "2500000000000",
            "PERatio": "28.5",
            "EPS": "5.25",
            "RevenueTTM": "394000000000",
            "ProfitMargin": "0.25",
            "DividendYield": "0.0062"
        }
        mock_service.return_value = mock_instance
        
        result = get_company_fundamentals.invoke({"symbol": "AAPL"})
        
        assert "COMPANY FUNDAMENTALS" in result
        assert "Apple Inc" in result
        assert "Technology" in result
        assert "P/E Ratio" in result
        assert "$2500.00B" in result or "2500" in result
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_fundamentals_with_na_values(self, mock_service):
        """Test handling of N/A values in fundamentals"""
        mock_instance = Mock()
        mock_instance.get_company_overview.return_value = {
            "Symbol": "TEST",
            "Name": "Test Company",
            "Sector": "N/A",
            "MarketCapitalization": "N/A",
            "PERatio": "N/A"
        }
        mock_service.return_value = mock_instance
        
        result = get_company_fundamentals.invoke({"symbol": "TEST"})
        
        assert "Test Company" in result
        assert "N/A" in result  # Should handle N/A gracefully
    
    def test_tool_has_description(self):
        """Test that tool has comprehensive description"""
        assert hasattr(get_company_fundamentals, 'description')
        description = get_company_fundamentals.description
        
        assert "fundamental" in description.lower()
        assert "P/E" in description or "ratio" in description.lower()
        assert "when to use" in description.lower()


class TestFinancialNewsSentimentTool:
    """Tests for get_financial_news_sentiment tool"""
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_successful_news_retrieval(self, mock_service):
        """Test successful news retrieval"""
        mock_instance = Mock()
        mock_instance.get_news_sentiment.return_value = {
            "feed": [
                {
                    "title": "Apple announces new product",
                    "summary": "Apple unveiled new products today.",
                    "time_published": "20250110T120000",
                    "source": "TechNews",
                    "overall_sentiment_score": 0.35,
                    "overall_sentiment_label": "Bullish",
                    "relevance_score": "0.8"
                },
                {
                    "title": "Market reacts to Apple earnings",
                    "summary": "Investors respond to quarterly results.",
                    "time_published": "20250109T150000",
                    "source": "FinanceDaily",
                    "overall_sentiment_score": 0.15,
                    "overall_sentiment_label": "Somewhat-Bullish",
                    "relevance_score": "0.9"
                }
            ]
        }
        mock_service.return_value = mock_instance
        
        result = get_financial_news_sentiment.invoke({"tickers": "AAPL", "limit": 10})
        
        assert "FINANCIAL NEWS & SENTIMENT" in result
        assert "AAPL" in result
        assert "Apple announces new product" in result
        assert "Bullish" in result
        assert "Articles Found: 2" in result
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_news_rate_limit(self, mock_service):
        """Test handling of rate limit for news endpoint"""
        mock_instance = Mock()
        mock_instance.get_news_sentiment.side_effect = RateLimitError("Premium feature")
        mock_service.return_value = mock_instance
        
        result = get_financial_news_sentiment.invoke({"tickers": "AAPL", "limit": 10})
        
        assert "Rate limit" in result or "Premium" in result
    
    @patch('tools.alpha_vantage_tools.AlphaVantageService')
    def test_empty_news_feed(self, mock_service):
        """Test handling of empty news feed"""
        mock_instance = Mock()
        mock_instance.get_news_sentiment.return_value = {"feed": []}
        mock_service.return_value = mock_instance
        
        result = get_financial_news_sentiment.invoke({"tickers": "RARE", "limit": 10})
        
        assert "No recent news" in result
    
    def test_tool_has_description(self):
        """Test that tool has comprehensive description"""
        assert hasattr(get_financial_news_sentiment, 'description')
        description = get_financial_news_sentiment.description
        
        assert "news" in description.lower()
        assert "sentiment" in description.lower()
        assert "when to use" in description.lower()


class TestToolMetadata:
    """Test all tools have proper metadata"""
    
    def test_all_tools_have_names(self):
        """Test that all tools have names"""
        tools = [
            get_live_stock_price,
            get_historical_stock_data,
            get_company_fundamentals,
            get_financial_news_sentiment
        ]
        
        for tool in tools:
            assert hasattr(tool, 'name')
            assert isinstance(tool.name, str)
            assert len(tool.name) > 0
    
    def test_all_tools_have_descriptions(self):
        """Test that all tools have comprehensive descriptions"""
        tools = [
            get_live_stock_price,
            get_historical_stock_data,
            get_company_fundamentals,
            get_financial_news_sentiment
        ]
        
        for tool in tools:
            assert hasattr(tool, 'description')
            description = tool.description
            
            # Each description should have key sections
            assert len(description) > 200  # Comprehensive description
            assert "when to use" in description.lower()
            
            # Should mention what NOT to use it for
            assert "when not to use" in description.lower() or "not" in description.lower()
    
    def test_tools_distinguish_data_types(self):
        """Test that tools clearly label their data type (LIVE vs HISTORICAL)"""
        # Live stock price should mention LIVE
        assert "LIVE" in get_live_stock_price.description or "current" in get_live_stock_price.description.lower()
        
        # Historical data should mention HISTORICAL
        assert "HISTORICAL" in get_historical_stock_data.description or "historical" in get_historical_stock_data.description.lower()
        
        # Fundamentals should be clear about its purpose
        assert "fundamental" in get_company_fundamentals.description.lower()
        
        # News should mention recent/live
        assert "news" in get_financial_news_sentiment.description.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
