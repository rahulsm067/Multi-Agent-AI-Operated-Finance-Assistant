from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from data_ingestion.scraper import FinancialScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler("scraping_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("scraping_agent")

app = FastAPI(
    title="Scraping Agent",
    description="Microservice for scraping filings, market sentiment, and yield data.",
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

scraper = FinancialScraper()

class ScrapingRequest(BaseModel):
    symbol: Optional[str] = None
    region: Optional[str] = None

@app.get("/health", tags=["Utility"])
async def health_check():
    """Health check endpoint."""
    logger.info("Health check called.")
    return {"status": "healthy"}

@app.get("/market-sentiment/{region}", tags=["Sentiment"])
async def get_market_sentiment(region: str):
    """Scrape market sentiment indicators for a region."""
    logger.info(f"/market-sentiment/{region} called.")
    try:
        sentiment = scraper.get_market_sentiment(region)
        logger.info(f"Sentiment result: {sentiment}")
        return sentiment
    except Exception as e:
        logger.error(f"Error in /market-sentiment/{region}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/company-filings/{symbol}", tags=["Filings"])
async def get_company_filings(symbol: str):
    """Get recent company filings for a symbol."""
    logger.info(f"/company-filings/{symbol} called.")
    try:
        filings = scraper.get_company_filings(symbol)
        logger.info(f"Filings result: {filings}")
        return {"filings": filings}
    except Exception as e:
        logger.error(f"Error in /company-filings/{symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/yield-data", tags=["Yield"])
async def get_yield_data():
    """Get current yield data."""
    logger.info("/yield-data called.")
    try:
        data = scraper.get_yield_data()
        logger.info(f"Yield data: {data}")
        return data
    except Exception as e:
        logger.error(f"Error in /yield-data: {e}")
        raise HTTPException(status_code=500, detail=str(e))