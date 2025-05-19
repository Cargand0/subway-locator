# subway_locator/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import endpoints

app = FastAPI(title="Subway Outlet Locator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(endpoints.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Subway Outlet Locator API", "docs_url": "/docs"}

# Ensure the database is created
from ..database.database import Base, engine
Base.metadata.create_all(bind=engine)