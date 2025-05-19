import argparse

def run_scraper():
    from subway_locator.scraper import main
    main.run()

def run_geocoder():
    from subway_locator.utils.geocoder import run
    run()

def run_api():
    import uvicorn
    uvicorn.run("subway_locator.api.main:app", host="0.0.0.0", port=8000, reload=True)

def run_frontend():
    from subway_locator.frontend import app
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Subway Outlet Locator')
    parser.add_argument('component', choices=['scraper', 'geocoder', 'api', 'frontend'],
                        help='Component to run')
    
    args = parser.parse_args()
    
    if args.component == 'scraper':
        run_scraper()
    elif args.component == 'geocoder':
        run_geocoder()
    elif args.component == 'api':
        run_api()
    elif args.component == 'frontend':
        run_frontend()
