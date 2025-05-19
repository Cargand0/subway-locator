# subway_locator/frontend/app.py
from flask import Flask, render_template, jsonify, request
import os
import requests

app = Flask(__name__)

# Configuration
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

@app.route('/')
def index():
    return render_template('index.html', api_base_url=API_BASE_URL)

@app.route('/api/outlets')
def get_outlets():
    """Proxy to backend API to avoid CORS issues during development"""
    geocoded_only = request.args.get('geocoded_only', 'true')
    response = requests.get(f"{API_BASE_URL}/outlets?geocoded_only={geocoded_only}")
    return jsonify(response.json())

@app.route('/api/search/<query>')
def search_outlets(query):
    """Proxy for searching outlets by name/location"""
    response = requests.get(f"{API_BASE_URL}/outlets/search/{query}")
    return jsonify(response.json())

@app.route('/api/location/<location>')
def location_outlets(location):
    """Proxy for getting outlets in a specific location"""
    response = requests.get(f"{API_BASE_URL}/outlets/location/{location}")
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)