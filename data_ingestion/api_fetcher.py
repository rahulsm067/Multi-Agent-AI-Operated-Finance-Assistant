import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("api_agent.fetcher")

class MarketDataFetcher:
    """
    Fetches and processes market data for the API Agent.
    Includes caching, error handling, and logging for all operations.
    """
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(minutes=15)

    def get_stock_data(self, symbol: str) -> Optional[Dict]:
        """Fetch current stock data from Yahoo Finance."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            result = {
                'symbol': symbol,
                'price': info.get('regularMarketPrice'),
                'change': info.get('regularMarketChangePercent'),
                'volume': info.get('regularMarketVolume'),
                'timestamp': datetime.now().isoformat()
            }
            logger.info(f"Fetched stock data for {symbol}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None

    def get_asia_tech_exposure(self, portfolio: List[Dict]) -> Dict:
        """Calculate Asia tech exposure from portfolio."""
        try:
            total_aum = sum(position['value'] for position in portfolio)
            asia_tech_value = sum(
                position['value'] for position in portfolio
                if position.get('region') == 'Asia' and position.get('sector') == 'Technology'
            )
            result = {
                'exposure_percentage': (asia_tech_value / total_aum * 100) if total_aum > 0 else 0,
                'total_value': asia_tech_value
            }
            logger.info(f"Calculated Asia tech exposure: {result}")
            return result
        except Exception as e:
            logger.error(f"Error calculating Asia tech exposure: {e}")
            return {'exposure_percentage': 0, 'total_value': 0}

    def get_earnings_surprises(self, symbols: List[str]) -> List[Dict]:
        """Get earnings surprises for given symbols."""
        surprises = []
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                earnings = ticker.earnings
                if earnings is not None and not earnings.empty:
                    latest = earnings.iloc[-1]
                    expected = latest.get('Expected')
                    actual = latest.get('Actual')
                    if expected and actual:
                        surprise_pct = ((actual - expected) / expected) * 100
                        surprise = {
                            'symbol': symbol,
                            'surprise_percentage': surprise_pct,
                            'actual': actual,
                            'expected': expected
                        }
                        surprises.append(surprise)
                        logger.info(f"Earnings surprise for {symbol}: {surprise}")
            except Exception as e:
                logger.error(f"Error fetching earnings data for {symbol}: {e}")
                continue
        return surprises