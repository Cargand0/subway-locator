from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.database import get_db
from ..database.models import SubwayOutlet
from pydantic import BaseModel

router = APIRouter()

# Pydantic model for API responses
class OutletResponse(BaseModel):
    id: int
    name: str
    address: str = None
    operating_hours: str = None
    waze_link: str = None
    latitude: float = None
    longitude: float = None
    
    class Config:
        orm_mode = True

@router.get("/outlets", response_model=List[OutletResponse])
def get_outlets(
    geocoded_only: bool = Query(False, description="Filter to only return outlets with coordinates"),
    db: Session = Depends(get_db)
):
    """Get all outlets"""
    query = db.query(SubwayOutlet)
    
    if geocoded_only:
        query = query.filter(
            SubwayOutlet.latitude.isnot(None),
            SubwayOutlet.longitude.isnot(None)
        )
    
    outlets = query.all()
    return outlets

@router.get("/outlets/{outlet_id}", response_model=OutletResponse)
def get_outlet(outlet_id: int, db: Session = Depends(get_db)):
    """Get a specific outlet by ID"""
    outlet = db.query(SubwayOutlet).filter(SubwayOutlet.id == outlet_id).first()
    if outlet is None:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return outlet

@router.get("/outlets/search/{query}")
def search_outlets(query: str, db: Session = Depends(get_db)):
    """Search outlets by name or location"""
    search_query = f"%{query}%"
    outlets = db.query(SubwayOutlet).filter(
        SubwayOutlet.name.ilike(search_query)
    ).all()
    return outlets

@router.get("/outlets/location/{location}")
def outlets_by_location(location: str, db: Session = Depends(get_db)):
    """Get outlets by location name"""
    search_location = f"%{location}%"
    outlets = db.query(SubwayOutlet).filter(
        SubwayOutlet.name.ilike(search_location)
    ).all()
    
    return {
        "location": location,
        "count": len(outlets),
        "outlets": outlets
    }

@router.get("/outlets/latest-closing")
def get_latest_closing_outlets(db: Session = Depends(get_db)):
    """Get outlets that close the latest"""
    # This is a simplified version - in reality, you would need to parse
    # the operating hours strings and compare them
    outlets = db.query(SubwayOutlet).order_by(SubwayOutlet.operating_hours.desc()).limit(5).all()
    return outlets