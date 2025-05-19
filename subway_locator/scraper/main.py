# subway_locator/scraper/main.py
import logging
import os
from .scraper import SubwayScraper
from sqlalchemy.orm import Session
from ..database.database import engine, Base, SessionLocal
from ..database.models import SubwayOutlet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_tables():
    """Create database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

def store_outlets(outlets, db: Session):
    """Store outlet data in the database"""
    # First, clear existing data
    db.query(SubwayOutlet).delete()
    logger.info("Cleared existing outlets from database")
    
    for outlet_data in outlets:
        outlet = SubwayOutlet(
            name=outlet_data.get("name", "Unknown"),
            address=outlet_data.get("address", ""),
            operating_hours=outlet_data.get("operating_hours", ""),
            waze_link=outlet_data.get("waze_link", "")
        )
        db.add(outlet)
    
    db.commit()
    logger.info(f"Stored {len(outlets)} outlets in database")

def run():
    """Run the scraper and store the data"""
    logger.info("Starting the scraping process")
    
    # Create debug directory
    os.makedirs("debug", exist_ok=True)
    
    # Create database tables
    create_tables()
    
    # Initialize scraper and get outlets
    scraper = SubwayScraper()
    outlets = scraper.scrape_outlets()
    
    if outlets:
        # Store the outlets in the database
        db = SessionLocal()
        try:
            store_outlets(outlets, db)
        finally:
            db.close()
        
        logger.info("Scraping and data storage completed successfully")
    else:
        logger.warning("No outlets were scraped")
        
        # Try to display some debug info about what might be wrong
        debug_files = os.listdir("debug") if os.path.exists("debug") else []
        if debug_files:
            logger.info(f"Debug files available in the debug folder: {', '.join(debug_files)}")
            logger.info("Check these files to understand what might be wrong with the scraping process")
        
        # Suggestions for troubleshooting
        logger.info("Troubleshooting suggestions:")
        logger.info("1. Check if the website structure has changed")
        logger.info("2. Try running without headless mode to see what's happening")
        logger.info("3. Check if there are captchas or other anti-bot measures")
        logger.info("4. Make sure you have a stable internet connection")

if __name__ == "__main__":
    run()