# subway_locator/utils/geocoder.py
import logging
import time
from geopy.geocoders import Nominatim
from sqlalchemy.orm import Session
from ..database.database import SessionLocal
from ..database.models import SubwayOutlet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Geocoder:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="subway_locator")
    
    def geocode_address(self, address):
        """Geocode a single address to get coordinates"""
        try:
            # Add "Malaysia" to the address if not present
            if "malaysia" not in address.lower():
                address = f"{address}, Malaysia"
            
            location = self.geolocator.geocode(address)
            
            if location:
                logger.info(f"Geocoded {address}: ({location.latitude}, {location.longitude})")
                return location.latitude, location.longitude
            else:
                logger.warning(f"Could not geocode address: {address}")
                return None, None
                
        except Exception as e:
            logger.error(f"Error geocoding address {address}: {str(e)}")
            return None, None
    
    def geocode_all_outlets(self):
        """Geocode all outlets in the database"""
        db = SessionLocal()
        try:
            # Get all outlets without coordinates
            outlets = db.query(SubwayOutlet).filter(
                (SubwayOutlet.latitude.is_(None)) | 
                (SubwayOutlet.longitude.is_(None))
            ).all()
            
            logger.info(f"Found {len(outlets)} outlets to geocode")
            
            for outlet in outlets:
                query = None
                
                # Try to geocode based on the outlet name if no address
                if not outlet.address:
                    # Extract location from name - replace "Subway" with empty string
                    location_name = outlet.name.replace("Subway", "").strip()
                    
                    # If it's too short, it's probably not specific enough
                    if len(location_name) > 2:
                        query = f"{location_name}, Kuala Lumpur, Malaysia"
                        logger.info(f"Using outlet name for geocoding: {query}")
                else:
                    query = outlet.address
                    
                # Skip if no query
                if not query:
                    logger.warning(f"Outlet {outlet.name} has no location info to geocode")
                    continue
                
                # Geocode the address/name
                lat, lng = self.geocode_address(query)
                
                # Update the outlet if geocoding succeeded
                if lat and lng:
                    outlet.latitude = lat
                    outlet.longitude = lng
                    db.commit()
                    logger.info(f"Updated coordinates for {outlet.name} using query: {query}")
                
                # Sleep to avoid hitting API rate limits
                time.sleep(1)
            
            # Count how many outlets have coordinates
            geocoded_count = db.query(SubwayOutlet).filter(
                SubwayOutlet.latitude.isnot(None),
                SubwayOutlet.longitude.isnot(None)
            ).count()
            
            logger.info(f"Geocoding completed. {geocoded_count} outlets have coordinates.")
            
        except Exception as e:
            logger.error(f"Error during geocoding: {str(e)}")
        finally:
            db.close()

def run():
    """Run the geocoding process"""
    logger.info("Starting geocoding process")
    geocoder = Geocoder()
    geocoder.geocode_all_outlets()
    logger.info("Geocoding process completed")

if __name__ == "__main__":
    run()