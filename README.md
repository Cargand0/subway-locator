# Subway Outlet Locator - Kuala Lumpur
A comprehensive application for finding and visualizing Subway restaurant locations throughout Kuala Lumpur, Malaysia.

## 📋 Features
* Interactive Map Visualization: View all Subway outlets across Kuala Lumpur with custom markers
* Catchment Area Analysis: Display 5KM radius catchment areas around each outlet
* Overlapping Areas Highlighting: Identify areas served by multiple Subway outlets
* Natural Language Search: Find outlets using plain language queries
* Advanced Filtering: Search by location, operating hours, and other criteria
* Detailed Outlet Information: Access complete information about each outlet
* RESTful API: Full-featured API for programmatic access to outlet data

---

## 🛠️ Technology Stack
* Backend: Python, FastAPI
* Frontend: Flask, HTML, CSS, JavaScript
* Mapping: Leaflet.js
* Data Collection: Selenium WebDriver
* Geocoding: Nominatim service
* Database: SQLite/JSON (for data storage)

---

## 🚀 Installation
### Prerequisites
* Python 3.8+
* Git

---

## Setup Instructions
1. Clone the repository
```bash
git clone https://github.com/yourusername/subway-outlet-locator.git
cd subway-outlet-locator
```

2. Set up a virtual environment
```bash
python -m venv venv

venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Configure environment variables
```bash
# Create a .env file with required variables
cp .env.example .env
# Edit .env file with your settings
```
5. Run data collection (if needed)
```bash

python -m src.data_collection.scraper
```
6. Start the API server
```bash
python -m src.api.main
```
7. Start the web application
```bash
python -m src.frontend.app
```
8. Access the application
Open your browser and go to http://localhost:5000

---

## 🗂️ Project Structure
```
subway-outlet-locator/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── __init__.py
│   ├── data_collection/
│   │   ├── __init__.py
│   │   └── scraper.py
│   ├── geocoding/
│   │   ├── __init__.py
│   │   └── geocoder.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── frontend/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── static/
│   │   └── templates/
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
└── tests/
    ├── __init__.py
    └── test_*.py
```

---

## 📖 API Documentation
### Endpoints
* GET /api/outlets - Get all outlets
* GET /api/outlets/{id} - Get outlet by ID
* GET /api/outlets/search - Search outlets by query parameters
* GET /api/outlets/near - Find outlets near coordinates

---

## Run Instructions
1. Run the API server
```bash
python run.py api
```

2. Run the web application
```bash
python run.py frontend
```