Subway Outlet Locator - Kuala Lumpur
A comprehensive application for finding and visualizing Subway restaurant locations throughout Kuala Lumpur, Malaysia.

Subway Outlet Map

📋 Features
Interactive Map Visualization: View all Subway outlets across Kuala Lumpur with custom markers
Catchment Area Analysis: Display 5KM radius catchment areas around each outlet
Overlapping Areas Highlighting: Identify areas served by multiple Subway outlets
Natural Language Search: Find outlets using plain language queries
Advanced Filtering: Search by location, operating hours, and other criteria
Detailed Outlet Information: Access complete information about each outlet
RESTful API: Full-featured API for programmatic access to outlet data
🛠️ Technology Stack
Backend: Python, FastAPI
Frontend: Flask, HTML, CSS, JavaScript
Mapping: Leaflet.js
Data Collection: Selenium WebDriver
Geocoding: Nominatim service
Database: SQLite/JSON (for data storage)
🚀 Installation
Prerequisites
Python 3.8+
Git
Setup Instructions
Clone the repository

BASH

git clone https://github.com/yourusername/subway-outlet-locator.git
cd subway-outlet-locator
Set up a virtual environment

BASH

python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
Install dependencies

BASH

pip install -r requirements.txt
Configure environment variables

BASH

# Create a .env file with required variables
cp .env.example .env
# Edit .env file with your settings
Run data collection (if needed)

BASH

python -m src.data_collection.scraper
Start the API server

BASH

python -m src.api.main
Start the web application

BASH

python -m src.frontend.app
Access the application
Open your browser and go to http://localhost:5000

🗂️ Project Structure

Collapse
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
📖 API Documentation
Endpoints
GET /api/outlets - Get all outlets
GET /api/outlets/{id} - Get outlet by ID
GET /api/outlets/search - Search outlets by query parameters
GET /api/outlets/near - Find outlets near coordinates
Example API Usage
Python

import requests

# Get all outlets
response = requests.get("http://localhost:8000/api/outlets")
outlets = response.json()

# Search for outlets
params = {"location": "KLCC", "radius": 3}
search_results = requests.get("http://localhost:8000/api/outlets/search", params=params).json()
🔍 Usage Examples
Finding the Nearest Outlet
Navigate to the web application
Use the search bar: "Find the nearest Subway to Petronas Towers"
View the results on the map with the nearest outlet highlighted
Analyzing Outlet Coverage
Enable catchment area visualization using the layer control
Identify overlapping areas (highlighted in darker colors)
Spot areas with limited Subway coverage
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Subway Malaysia for their restaurant network
OpenStreetMap and Nominatim for geocoding services
The open-source community for the amazing tools and libraries
Note: This project is not officially affiliated with Subway® restaurants. It was created for educational and research purposes.
