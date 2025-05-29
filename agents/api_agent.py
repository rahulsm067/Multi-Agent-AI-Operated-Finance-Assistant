from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import logging
from data_ingestion.api_fetcher import MarketDataFetcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler("api_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("api_agent")

app = FastAPI(
    title="API Agent",
    description="Microservice for real-time & historical market data via Yahoo Finance/AlphaVantage.",
    version="1.0.0"
)

# Enable CORS for local development and Streamlit UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

market_data_fetcher = MarketDataFetcher()

class Portfolio(BaseModel):
    positions: List[Dict]

class SymbolList(BaseModel):
    symbols: List[str]

@app.get("/health", tags=["Utility"])
async def health_check():
    """Health check endpoint."""
    logger.info("Health check called.")
    return {"status": "healthy"}

@app.post("/asia-tech-exposure", tags=["Portfolio"])
async def get_asia_tech_exposure(portfolio: Portfolio):
    """Calculate Asia tech exposure from portfolio positions."""
    logger.info(f"/asia-tech-exposure called with positions: {portfolio.positions}")
    try:
        exposure = market_data_fetcher.get_asia_tech_exposure(portfolio.positions)
        logger.info(f"Exposure result: {exposure}")
        return exposure
    except Exception as e:
        logger.error(f"Error in /asia-tech-exposure: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/earnings-surprises", tags=["Earnings"])
async def get_earnings_surprises(symbols: SymbolList):
    """Get earnings surprises for a list of symbols."""
    logger.info(f"/earnings-surprises called with symbols: {symbols.symbols}")
    try:
        surprises = market_data_fetcher.get_earnings_surprises(symbols.symbols)
        logger.info(f"Earnings surprises: {surprises}")
        return {"surprises": surprises}
    except Exception as e:
        logger.error(f"Error in /earnings-surprises: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock/{symbol}", tags=["Stock"])
async def get_stock_data(symbol: str):
    """Fetch current stock data for a given symbol."""
    logger.info(f"/stock/{symbol} called.")
    data = market_data_fetcher.get_stock_data(symbol)
    if data is None:
        logger.warning(f"Data not found for symbol {symbol}")
        raise HTTPException(status_code=404, detail=f"Data not found for symbol {symbol}")
    logger.info(f"Stock data: {data}")
    return data