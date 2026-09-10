"""
Alpha Vantage API Service
Provides a clean interface for interacting with Alpha Vantage financial data API.
Handles API key management, error handling, and rate limiting.
"""

import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AlphaVantageError(Exception):
    """Base exception for Alpha Vantage API errors."""
    pass


class APIKeyMissingError(AlphaVantageError):
    """Raised when API key is not configured."""
    pass


class InvalidSymbolError(AlphaVantageError):
    """Raised when an invalid stock symbol is provided."""
    pass


class RateLimitError(AlphaVantageError):
    """Raised when API rate limit is exceeded."""
    pass


class APIResponseError(AlphaVantageError):
    """Raised when API returns an unexpected response."""
    pass


class AlphaVantageService:
    """
    Service class for Alpha Vantage API interactions.
    
    Provides methods for:
    - Stock quotes
    - Historical data
    - Company fundamentals
    - News and sentiment
    
    Handles error cases gracefully without crashing the application.
    """
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Alpha Vantage service.
        
        Args:
            api_key: API key for Alpha Vantage. If not provided, reads from
                    ALPHA_VANTAGE_API_KEY environment variable.
        
        Raises:
            APIKeyMissingError: If no API key is found.
        """
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        
        if not self.api_key:
            raise APIKeyMissingError(
                "Alpha Vantage API key not found. "
                "Please set ALPHA_VANTAGE_API_KEY environment variable "
                "or pass api_key to the constructor."
            )
    
    def _make_request(
        self, 
        function: str, 
        params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to Alpha Vantage API.
        
        Args:
            function: Alpha Vantage API function name
            params: Additional query parameters
        
        Returns:
            Parsed JSON response
        
        Raises:
            RateLimitError: If rate limit is exceeded
            APIResponseError: If response is invalid or contains an error
        """
        query_params = {
            "function": function,
            "apikey": self.api_key
        }
        
        if params:
            query_params.update(params)
        
        try:
            response = requests.get(
                self.BASE_URL,
                params=query_params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API error messages
            if "Error Message" in data:
                error_msg = data["Error Message"]
                if "Invalid API call" in error_msg or "invalid" in error_msg.lower():
                    raise InvalidSymbolError(f"Invalid request: {error_msg}")
                raise APIResponseError(f"API Error: {error_msg}")
            
            # Check for rate limit message
            if "Note" in data:
                note = data["Note"]
                if "API call frequency" in note or "premium" in note.lower():
                    raise RateLimitError(
                        "API rate limit exceeded. Please try again later or upgrade your plan."
                    )
            
            # Check for Information message (often indicates limits)
            if "Information" in data:
                info = data["Information"]
                if "premium" in info.lower() or "higher API" in info:
                    raise RateLimitError(f"API limitation: {info}")
            
            return data
            
        except requests.exceptions.Timeout:
            raise APIResponseError("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise APIResponseError(f"Network error: {str(e)}")
        except ValueError as e:
            raise APIResponseError(f"Invalid JSON response: {str(e)}")
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time quote for a stock symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        
        Returns:
            Dictionary containing:
                - symbol: Stock symbol
                - price: Current price
                - change: Price change
                - change_percent: Percentage change
                - volume: Trading volume
                - latest_trading_day: Last trading day
        
        Raises:
            InvalidSymbolError: If symbol is invalid
            RateLimitError: If rate limit exceeded
            APIResponseError: If API returns unexpected response
        """
        if not symbol or not isinstance(symbol, str):
            raise InvalidSymbolError("Symbol must be a non-empty string")
        
        symbol = symbol.strip().upper()
        
        data = self._make_request("GLOBAL_QUOTE", {"symbol": symbol})
        
        # Check if quote data exists
        if "Global Quote" not in data:
            raise APIResponseError("Quote data not found in response")
        
        quote = data["Global Quote"]
        
        # Check if quote is empty (invalid symbol)
        if not quote:
            raise InvalidSymbolError(f"No data found for symbol: {symbol}")
        
        return {
            "symbol": quote.get("01. symbol", symbol),
            "price": float(quote.get("05. price", 0)),
            "change": float(quote.get("09. change", 0)),
            "change_percent": quote.get("10. change percent", "0%").rstrip("%"),
            "volume": int(quote.get("06. volume", 0)),
            "latest_trading_day": quote.get("07. latest trading day", "N/A")
        }
    
    def get_time_series_daily(
        self, 
        symbol: str, 
        outputsize: str = "compact"
    ) -> Dict[str, Any]:
        """
        Get daily historical price data for a stock.
        
        Args:
            symbol: Stock ticker symbol
            outputsize: 'compact' (last 100 data points) or 'full' (20+ years)
        
        Returns:
            Dictionary containing:
                - symbol: Stock symbol
                - time_series: Dict of date -> OHLCV data
                - meta_data: Information about the data
        
        Raises:
            InvalidSymbolError: If symbol is invalid
            RateLimitError: If rate limit exceeded
            APIResponseError: If API returns unexpected response
        """
        if not symbol or not isinstance(symbol, str):
            raise InvalidSymbolError("Symbol must be a non-empty string")
        
        symbol = symbol.strip().upper()
        
        params = {
            "symbol": symbol,
            "outputsize": outputsize
        }
        
        data = self._make_request("TIME_SERIES_DAILY", params)
        
        # Check if time series data exists
        if "Time Series (Daily)" not in data:
            raise APIResponseError("Time series data not found in response")
        
        return {
            "symbol": symbol,
            "time_series": data["Time Series (Daily)"],
            "meta_data": data.get("Meta Data", {})
        }
    
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """
        Get company fundamentals and overview information.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary containing company information including:
                - symbol: Stock symbol
                - name: Company name
                - description: Business description
                - sector: Industry sector
                - market_cap: Market capitalization
                - pe_ratio: Price-to-earnings ratio
                - eps: Earnings per share
                - dividend_yield: Dividend yield
                - revenue: Annual revenue
                - And many other fundamental metrics
        
        Raises:
            InvalidSymbolError: If symbol is invalid
            RateLimitError: If rate limit exceeded
            APIResponseError: If API returns unexpected response
        """
        if not symbol or not isinstance(symbol, str):
            raise InvalidSymbolError("Symbol must be a non-empty string")
        
        symbol = symbol.strip().upper()
        
        data = self._make_request("OVERVIEW", {"symbol": symbol})
        
        # Check if overview data exists
        if "Symbol" not in data:
            if not data:
                raise InvalidSymbolError(f"No data found for symbol: {symbol}")
            raise APIResponseError("Company overview data not found in response")
        
        # Return the full overview (contains many fields)
        return data
    
    def get_news_sentiment(
        self, 
        tickers: Optional[str] = None,
        topics: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get news articles and sentiment data.
        
        Note: This endpoint may not be available on all API plans.
        
        Args:
            tickers: Comma-separated stock symbols (e.g., "AAPL,MSFT")
            topics: Topic filter (e.g., "technology", "earnings")
            limit: Maximum number of articles (default 50)
        
        Returns:
            Dictionary containing:
                - feed: List of news articles with sentiment scores
                - sentiment_score_definition: Description of scoring
        
        Raises:
            RateLimitError: If rate limit exceeded or feature not available
            APIResponseError: If API returns unexpected response
        """
        params = {"limit": str(limit)}
        
        if tickers:
            params["tickers"] = tickers.upper()
        
        if topics:
            params["topics"] = topics
        
        try:
            data = self._make_request("NEWS_SENTIMENT", params)
            
            # Check if news data exists
            if "feed" not in data:
                raise APIResponseError("News data not found in response")
            
            return data
            
        except RateLimitError:
            # Re-raise rate limit errors
            raise
        except AlphaVantageError as e:
            # Wrap other errors with more context
            raise APIResponseError(
                f"News sentiment endpoint error: {str(e)}. "
                "This feature may require a premium API plan."
            )
    
    def health_check(self) -> bool:
        """
        Check if the API key is valid and service is accessible.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Try a lightweight request
            self.get_quote("AAPL")
            return True
        except AlphaVantageError:
            return False


# Convenience function for easy import
def get_alpha_vantage_service(api_key: Optional[str] = None) -> AlphaVantageService:
    """
    Factory function to create an AlphaVantageService instance.
    
    Args:
        api_key: Optional API key. If not provided, reads from environment.
    
    Returns:
        AlphaVantageService instance
    
    Raises:
        APIKeyMissingError: If no API key is found
    """
    return AlphaVantageService(api_key=api_key)
