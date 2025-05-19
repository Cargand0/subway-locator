# subway_locator/database/models.py
from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class SubwayOutlet(Base):
    __tablename__ = "subway_outlets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(Text)
    operating_hours = Column(Text)
    waze_link = Column(String(512))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"<SubwayOutlet(name='{self.name}', address='{self.address}')>"