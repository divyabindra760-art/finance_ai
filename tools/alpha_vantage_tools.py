"""
Alpha Vantage Market Data Tools
Provides live and historical market data through Alpha Vantage API.
"""

from langchain.tools import tool
from typing import Optional
from services.alpha_vantage_service import (
    AlphaVantageService,
    AlphaVantageError,
    InvalidSymbolError,
    RateLimitError,
    APIResponseError
)


@tool
def get_live_stock_price(symbol: str) -> str:
    """
    Retrieve the latest available market price and real-time quote information for a publicly traded stock.
    
    This tool fetches LIVE/CURRENT market data from Alpha Vantage including the most recent price, 
    price change, volume, and latest trading day.
    
    WHEN TO USE THIS TOOL:
    - User asks for the "current" stock price
    - User asks for the "latest" price
    - User asks "what is [company]'s stock price?"
    - User asks "how is [ticker] trading today?"
    - User wants to know the most recent market price
    - Questions about current valuation or market cap calculation
    
    EXAMPLES OF QUERIES FOR THIS TOOL:
    - "What is Apple's current stock price?"
    - "How much is TSLA trading at?"
    - "What's the latest price for Microsoft stock?"
    - "Is AAPL up or down today?"
    - "Get me the current quote for NVDA"
    
    WHEN NOT TO USE THIS TOOL:
    - Historical price data (use historical market data tool instead)
    - Company fundamentals like P/E ratio or market cap (use company fundamentals tool)
    - Financial statements from documents (use financial document retrieval tool)
    - News about the company (use news/sentiment tool)
    - Questions about "past" or "historical" prices
    
    INPUT:
    - symbol (str): Stock ticker symbol (e.g., "AAPL", "MSFT", "TSLA")
      The symbol will be automatically normalized (uppercase, trimmed)
    
    OUTPUT:
    Returns a formatted string containing:
    - Stock symbol
    - Current price in USD
    - Price change (absolute and percentage)
    - Trading volume
    - Latest trading day
    - Clearly labeled as "LIVE MARKET DATA"
    
    IMPORTANT NOTES:
    - This returns LIVE/CURRENT market data, not historical information
    - Prices are delayed by API provider (typically 15-20 minutes for free tier)
    - Data is in USD for US stocks
    - Requires valid Alpha Vantage API key
    - Subject to API rate limits (5 calls/minute for free tier)
    - Invalid symbols will return an error message
    
    Args:
        symbol: Stock ticker symbol (e.g., "AAPL")
    
    Returns:
        Formatted string with current stock quote information
    """
    try:
        service = AlphaVantageService()
        quote = service.get_quote(symbol)
        
        # Format output with clear labeling
        output = []
        output.append("=" * 60)
        output.append("📈 LIVE STOCK QUOTE (CURRENT MARKET DATA)")
        output.append("=" * 60)
        output.append(f"\n🏢 Symbol: {quote['symbol']}")
        output.append(f"💵 Current Price: ${quote['price']:.2f} USD")
        
        change = quote['change']
        change_pct = quote['change_percent']
        direction = "📈" if change >= 0 else "📉"
        output.append(f"{direction} Change: ${change:+.2f} ({change_pct}%)")
        
        output.append(f"📊 Volume: {quote['volume']:,} shares")
        output.append(f"📅 Latest Trading Day: {quote['latest_trading_day']}")
        output.append("\n" + "=" * 60)
        output.append("⚠️  Note: This is LIVE market data from Alpha Vantage API.")
        output.append("    Prices may be delayed 15-20 minutes for free tier.")
        output.append("=" * 60)
        
        return "\n".join(output)
        
    except InvalidSymbolError as e:
        return f"❌ Invalid stock symbol: {str(e)}\n\nPlease check the ticker symbol and try again."
    except RateLimitError as e:
        return f"⏱️  Rate limit exceeded: {str(e)}\n\nPlease wait a moment before trying again."
    except AlphaVantageError as e:
        return f"❌ Error fetching stock quote: {str(e)}"


@tool
def get_historical_stock_data(symbol: str, period: str = "compact") -> str:
    """
    Retrieve historical daily price data for a stock to analyze past performance and price movements.
    
    This tool fetches HISTORICAL time-series market data including open, high, low, close prices and volume
    for each trading day. Use this when analyzing past performance, trends, or price movements.
    
    WHEN TO USE THIS TOOL:
    - User asks about historical stock performance
    - User asks "how has [stock] performed over time?"
    - Questions about past price movements
    - User wants to see price trends
    - User asks about year-to-date performance
    - Questions involving "was" or "has been" regarding prices
    - Comparison of current vs past prices
    
    EXAMPLES OF QUERIES FOR THIS TOOL:
    - "How has Apple stock performed over the last year?"
    - "Show me Tesla's price history"
    - "What was Microsoft's stock price trend?"
    - "Has NVDA been going up or down lately?"
    - "How did Amazon perform in the past quarter?"
    
    WHEN NOT TO USE THIS TOOL:
    - Current/latest stock price (use live stock price tool instead)
    - Company fundamentals or financial ratios (use company fundamentals tool)
    - Financial data from annual reports (use financial document retrieval tool)
    - Recent news or events (use news/sentiment tool)
    
    INPUT:
    - symbol (str): Stock ticker symbol (e.g., "AAPL", "MSFT")
    - period (str): "compact" for last 100 days (default) or "full" for 20+ years
      (Note: "full" uses more API quota)
    
    OUTPUT:
    Returns a formatted string containing:
    - Stock symbol
    - Number of data points retrieved
    - Sample of recent trading days with OHLC data
    - Price trend summary (recent highs/lows)
    - Clearly labeled as "HISTORICAL MARKET DATA"
    
    IMPORTANT NOTES:
    - This returns HISTORICAL data, not current/live prices
    - Default returns last 100 trading days (compact mode)
    - Full history available but uses more API quota
    - Data is daily close prices (not intraday)
    - Requires valid Alpha Vantage API key
    - Subject to API rate limits
    
    Args:
        symbol: Stock ticker symbol
        period: "compact" (last 100 days) or "full" (20+ years)
    
    Returns:
        Formatted string with historical price data and trends
    """
    try:
        service = AlphaVantageService()
        data = service.get_time_series_daily(symbol, outputsize=period)
        
        time_series = data['time_series']
        dates = sorted(time_series.keys(), reverse=True)
        
        if not dates:
            return f"❌ No historical data found for {symbol}"
        
        # Calculate some basic statistics
        recent_dates = dates[:30]  # Last 30 days
        recent_closes = [float(time_series[d]['4. close']) for d in recent_dates]
        
        latest_price = recent_closes[0]
        highest = max(recent_closes)
        lowest = min(recent_closes)
        
        # Format output
        output = []
        output.append("=" * 60)
        output.append("📊 HISTORICAL STOCK DATA (PAST MARKET DATA)")
        output.append("=" * 60)
        output.append(f"\n🏢 Symbol: {symbol}")
        output.append(f"📅 Data Points: {len(dates)} trading days")
        output.append(f"📆 Date Range: {dates[-1]} to {dates[0]}")
        
        output.append(f"\n📈 Recent 30-Day Statistics:")
        output.append(f"   Latest Close: ${latest_price:.2f}")
        output.append(f"   30-Day High: ${highest:.2f}")
        output.append(f"   30-Day Low: ${lowest:.2f}")
        
        # Show last 5 trading days
        output.append(f"\n📋 Last 5 Trading Days:")
        for date in dates[:5]:
            day_data = time_series[date]
            close = float(day_data['4. close'])
            volume = int(float(day_data['5. volume']))
            output.append(f"   {date}: ${close:.2f} (Volume: {volume:,})")
        
        output.append("\n" + "=" * 60)
        output.append("⚠️  Note: This is HISTORICAL market data.")
        output.append("    For current prices, use the live stock price tool.")
        output.append("=" * 60)
        
        return "\n".join(output)
        
    except InvalidSymbolError as e:
        return f"❌ Invalid stock symbol: {str(e)}"
    except RateLimitError as e:
        return f"⏱️  Rate limit exceeded: {str(e)}"
    except AlphaVantageError as e:
        return f"❌ Error fetching historical data: {str(e)}"


@tool
def get_company_fundamentals(symbol: str) -> str:
    """
    Retrieve comprehensive company fundamental data including financial metrics, ratios, and business information.
    
    This tool fetches company overview and fundamental financial data such as market cap, P/E ratio, EPS,
    revenue, profit margins, dividend information, and business description. Use this for fundamental analysis.
    
    WHEN TO USE THIS TOOL:
    - User asks about company fundamentals or financial metrics
    - Questions about P/E ratio, EPS, market cap, or other ratios
    - User asks "what are [company]'s fundamentals?"
    - Questions about valuation metrics
    - Dividend information requests
    - Company sector, industry, or business description
    - Questions about company size or market position
    
    EXAMPLES OF QUERIES FOR THIS TOOL:
    - "What are Apple's fundamentals?"
    - "What is Microsoft's P/E ratio?"
    - "What's Tesla's market capitalization?"
    - "Does Amazon pay dividends?"
    - "What sector is NVDA in?"
    - "What are Google's earnings per share?"
    - "Is Apple overvalued?"
    
    WHEN NOT TO USE THIS TOOL:
    - Current stock prices (use live stock price tool instead)
    - Historical price movements (use historical market data tool instead)
    - Detailed financial statements from reports (use financial document retrieval tool)
    - Recent news or events (use news/sentiment tool)
    - Questions specifically about annual reports or 10-K filings
    
    INPUT:
    - symbol (str): Stock ticker symbol (e.g., "AAPL", "MSFT", "GOOGL")
    
    OUTPUT:
    Returns a formatted string containing:
    - Company name and description
    - Sector and industry
    - Market capitalization
    - Financial ratios (P/E, P/B, PEG, etc.)
    - Profitability metrics (profit margin, ROE, ROA)
    - Revenue and earnings data
    - Dividend information
    - Key business metrics
    - Clearly labeled as "COMPANY FUNDAMENTALS (API DATA)"
    
    IMPORTANT NOTES:
    - This returns fundamental data from Alpha Vantage API, not documents
    - Data is typically updated quarterly with earnings reports
    - Metrics are trailing twelve months (TTM) unless specified
    - Currency is USD for US stocks
    - Some metrics may be "None" if not applicable (e.g., non-dividend stocks)
    - Requires valid Alpha Vantage API key
    - Subject to API rate limits
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        Formatted string with company fundamentals and financial metrics
    """
    try:
        service = AlphaVantageService()
        overview = service.get_company_overview(symbol)
        
        # Format output
        output = []
        output.append("=" * 60)
        output.append("🏦 COMPANY FUNDAMENTALS & OVERVIEW")
        output.append("=" * 60)
        
        # Basic info
        output.append(f"\n🏢 Company: {overview.get('Name', 'N/A')}")
        output.append(f"🎯 Symbol: {overview.get('Symbol', symbol)}")
        output.append(f"🏭 Sector: {overview.get('Sector', 'N/A')}")
        output.append(f"🔧 Industry: {overview.get('Industry', 'N/A')}")
        output.append(f"🌍 Country: {overview.get('Country', 'N/A')}")
        
        # Description
        description = overview.get('Description', 'N/A')
        if description and description != 'N/A':
            output.append(f"\n📝 Business Description:")
            output.append(f"   {description[:300]}...")
        
        # Market metrics
        output.append(f"\n💰 Market Metrics:")
        market_cap = overview.get('MarketCapitalization', 'N/A')
        if market_cap != 'N/A' and market_cap:
            market_cap_b = int(market_cap) / 1_000_000_000
            output.append(f"   Market Cap: ${market_cap_b:.2f}B USD")
        else:
            output.append(f"   Market Cap: N/A")
        
        # Valuation ratios
        output.append(f"\n📊 Valuation Ratios:")
        output.append(f"   P/E Ratio: {overview.get('PERatio', 'N/A')}")
        output.append(f"   P/B Ratio: {overview.get('PriceToBookRatio', 'N/A')}")
        output.append(f"   PEG Ratio: {overview.get('PEGRatio', 'N/A')}")
        
        # Profitability
        output.append(f"\n💵 Profitability:")
        output.append(f"   EPS (TTM): ${overview.get('EPS', 'N/A')}")
        output.append(f"   Profit Margin: {overview.get('ProfitMargin', 'N/A')}")
        output.append(f"   ROE: {overview.get('ReturnOnEquityTTM', 'N/A')}")
        output.append(f"   ROA: {overview.get('ReturnOnAssetsTTM', 'N/A')}")
        
        # Revenue and earnings
        output.append(f"\n💼 Revenue & Earnings (TTM):")
        revenue = overview.get('RevenueTTM', 'N/A')
        if revenue != 'N/A' and revenue:
            revenue_b = int(revenue) / 1_000_000_000
            output.append(f"   Revenue: ${revenue_b:.2f}B USD")
        else:
            output.append(f"   Revenue: N/A")
        
        gross_profit = overview.get('GrossProfitTTM', 'N/A')
        if gross_profit != 'N/A' and gross_profit:
            gross_profit_b = int(gross_profit) / 1_000_000_000
            output.append(f"   Gross Profit: ${gross_profit_b:.2f}B USD")
        else:
            output.append(f"   Gross Profit: N/A")
        
        # Dividend info
        output.append(f"\n💸 Dividend Information:")
        output.append(f"   Dividend Yield: {overview.get('DividendYield', 'N/A')}")
        output.append(f"   Dividend Per Share: ${overview.get('DividendPerShare', 'N/A')}")
        output.append(f"   Ex-Dividend Date: {overview.get('ExDividendDate', 'N/A')}")
        
        # Additional metrics
        output.append(f"\n📈 Additional Metrics:")
        output.append(f"   Beta: {overview.get('Beta', 'N/A')}")
        output.append(f"   52-Week High: ${overview.get('52WeekHigh', 'N/A')}")
        output.append(f"   52-Week Low: ${overview.get('52WeekLow', 'N/A')}")
        
        output.append("\n" + "=" * 60)
        output.append("⚠️  Note: This is FUNDAMENTAL DATA from Alpha Vantage API.")
        output.append("    Metrics are typically updated quarterly with earnings.")
        output.append("=" * 60)
        
        return "\n".join(output)
        
    except InvalidSymbolError as e:
        return f"❌ Invalid stock symbol: {str(e)}"
    except RateLimitError as e:
        return f"⏱️  Rate limit exceeded: {str(e)}"
    except AlphaVantageError as e:
        return f"❌ Error fetching company fundamentals: {str(e)}"


@tool
def get_financial_news_sentiment(tickers: str, limit: int = 10) -> str:
    """
    Retrieve recent financial news articles and sentiment analysis for specified stock ticker(s).
    
    This tool fetches the latest news articles related to a company or stock along with AI-powered
    sentiment scores. Use this to understand recent events, market sentiment, and news that might
    affect stock performance.
    
    WHEN TO USE THIS TOOL:
    - User asks about recent news for a company
    - Questions about "what's happening with [company]?"
    - User wants to know market sentiment
    - Questions about recent events or announcements
    - User asks "why is [stock] moving?"
    - Questions about "latest news" or "recent developments"
    - Understanding potential catalysts or risks
    
    EXAMPLES OF QUERIES FOR THIS TOOL:
    - "What's the latest news about Apple?"
    - "Why is Tesla stock moving today?"
    - "What recent developments affect Microsoft?"
    - "Show me news about NVDA"
    - "What's the market sentiment on Amazon?"
    - "Are there any recent announcements from Google?"
    
    WHEN NOT TO USE THIS TOOL:
    - Current stock prices (use live stock price tool instead)
    - Historical price data (use historical market data tool instead)
    - Company fundamentals or ratios (use company fundamentals tool)
    - Financial data from annual reports (use financial document retrieval tool)
    - General company description (use company fundamentals tool)
    
    INPUT:
    - tickers (str): Stock ticker symbol or comma-separated symbols (e.g., "AAPL" or "AAPL,MSFT")
    - limit (int): Maximum number of articles to retrieve (default: 10, max: 50)
    
    OUTPUT:
    Returns a formatted string containing:
    - Number of articles found
    - For each article:
      - Title and summary
      - Publication date and source
      - Sentiment score and label (Bullish/Bearish/Neutral)
      - Relevance score
    - Overall sentiment summary
    - Clearly labeled as "FINANCIAL NEWS & SENTIMENT (LIVE DATA)"
    
    IMPORTANT NOTES:
    - This returns LIVE/RECENT news, updated continuously
    - Sentiment scores range from -1 (very bearish) to +1 (very bullish)
    - News articles are from various financial sources
    - This endpoint may require Premium Alpha Vantage plan
    - If not available, will return appropriate error message
    - Requires valid Alpha Vantage API key
    - Subject to API rate limits
    
    Args:
        tickers: Stock ticker symbol(s), comma-separated for multiple
        limit: Maximum number of articles (default 10)
    
    Returns:
        Formatted string with news articles and sentiment analysis
    """
    try:
        service = AlphaVantageService()
        news_data = service.get_news_sentiment(tickers=tickers, limit=limit)
        
        feed = news_data.get('feed', [])
        
        if not feed:
            return f"📰 No recent news found for {tickers}"
        
        # Format output
        output = []
        output.append("=" * 60)
        output.append("📰 FINANCIAL NEWS & SENTIMENT (LIVE DATA)")
        output.append("=" * 60)
        output.append(f"\n🎯 Tickers: {tickers}")
        output.append(f"📊 Articles Found: {len(feed)}")
        
        # Show articles
        for i, article in enumerate(feed[:limit], 1):
            output.append(f"\n--- Article {i} ---")
            output.append(f"📌 Title: {article.get('title', 'N/A')}")
            
            summary = article.get('summary', 'N/A')
            if summary and len(summary) > 200:
                summary = summary[:200] + "..."
            output.append(f"📝 Summary: {summary}")
            
            output.append(f"📅 Published: {article.get('time_published', 'N/A')}")
            output.append(f"🏢 Source: {article.get('source', 'N/A')}")
            
            # Sentiment
            sentiment_score = article.get('overall_sentiment_score', 0)
            sentiment_label = article.get('overall_sentiment_label', 'Neutral')
            
            if sentiment_score > 0.15:
                emoji = "📈"
            elif sentiment_score < -0.15:
                emoji = "📉"
            else:
                emoji = "➡️"
            
            output.append(f"{emoji} Sentiment: {sentiment_label} (Score: {sentiment_score:.3f})")
            
            relevance = article.get('relevance_score', 'N/A')
            output.append(f"🎯 Relevance: {relevance}")
        
        # Overall sentiment summary
        if len(feed) > 0:
            avg_sentiment = sum(a.get('overall_sentiment_score', 0) for a in feed) / len(feed)
            output.append(f"\n📊 Average Sentiment Score: {avg_sentiment:.3f}")
            
            if avg_sentiment > 0.15:
                output.append("📈 Overall: Bullish sentiment")
            elif avg_sentiment < -0.15:
                output.append("📉 Overall: Bearish sentiment")
            else:
                output.append("➡️  Overall: Neutral sentiment")
        
        output.append("\n" + "=" * 60)
        output.append("⚠️  Note: This is LIVE news data from Alpha Vantage.")
        output.append("    Sentiment scores: Bullish (+), Bearish (-), Neutral (~0)")
        output.append("=" * 60)
        
        return "\n".join(output)
        
    except RateLimitError as e:
        return (
            f"⏱️  Rate limit or plan restriction: {str(e)}\n\n"
            "Note: News/sentiment endpoint may require Premium Alpha Vantage plan."
        )
    except AlphaVantageError as e:
        return (
            f"❌ Error fetching news: {str(e)}\n\n"
            "Note: This endpoint may not be available on your Alpha Vantage plan."
        )


# Export all tools
__all__ = [
    'get_live_stock_price',
    'get_historical_stock_data',
    'get_company_fundamentals',
    'get_financial_news_sentiment'
]
