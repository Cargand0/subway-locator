import requests
from bs4 import BeautifulSoup
import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SubwayScraper:
    def __init__(self):
        self.base_url = "https://subway.com.my/find-a-subway"
        self.outlets = []
        
    def setup_driver(self):
        """Initialize the Selenium WebDriver with Chrome"""
        logger.info("Setting up Chrome WebDriver...")
        
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Add user agent to mimic a real browser
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        
        # Set up the Chrome driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver
    
    def scrape_outlets(self):
        """Scrape Subway outlets filtered for Kuala Lumpur"""
        logger.info("Starting to scrape Subway outlets...")
        
        driver = self.setup_driver()
        
        try:
            # Navigate to the Subway store locator page
            driver.get(self.base_url)
            logger.info("Navigated to Subway store locator page")
            
            # Wait longer for the page to load completely
            time.sleep(10)
            
            # Create debug directory if it doesn't exist
            os.makedirs("debug", exist_ok=True)
            
            # Take screenshot for debugging
            driver.save_screenshot("debug/initial_page.png")
            logger.info("Saved initial page screenshot")
            
            # Save page source for analysis
            with open("debug/initial_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            logger.info("Saved initial page source")
            
            # Look for the search input using multiple strategies
            search_input = None
            search_strategies = [
                (By.ID, "addressInput"),
                (By.NAME, "address"),
                (By.XPATH, "//input[@placeholder='Search by Postcode, City or State']"),
                (By.XPATH, "//input[contains(@class, 'search')]"),
                (By.CSS_SELECTOR, ".store-search-input"),
                (By.TAG_NAME, "input")
            ]
            
            for strategy in search_strategies:
                try:
                    elements = driver.find_elements(strategy[0], strategy[1])
                    logger.info(f"Strategy {strategy} found {len(elements)} elements")
                    
                    if elements:
                        for element in elements:
                            if element.is_displayed():
                                search_input = element
                                logger.info(f"Found visible search input using strategy {strategy}")
                                break
                                
                    if search_input:
                        break
                except Exception as e:
                    logger.warning(f"Strategy {strategy} failed: {str(e)}")
            
            if not search_input:
                logger.error("Could not find search input using any strategy")
                # Try to identify form elements to understand the page structure
                forms = driver.find_elements(By.TAG_NAME, "form")
                logger.info(f"Found {len(forms)} form elements")
                for i, form in enumerate(forms):
                    logger.info(f"Form {i} HTML: {form.get_attribute('outerHTML')}")
                
                # Try with iframes
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                logger.info(f"Found {len(iframes)} iframes")
                
                for i, iframe in enumerate(iframes):
                    try:
                        logger.info(f"Switching to iframe {i}")
                        driver.switch_to.frame(iframe)
                        
                        # Take screenshot inside iframe
                        driver.save_screenshot(f"debug/iframe_{i}.png")
                        
                        # Try to find search input inside iframe
                        for strategy in search_strategies:
                            try:
                                elements = driver.find_elements(strategy[0], strategy[1])
                                if elements and elements[0].is_displayed():
                                    search_input = elements[0]
                                    logger.info(f"Found search input in iframe {i} using strategy {strategy}")
                                    break
                            except:
                                pass
                        
                        # Switch back to main content
                        driver.switch_to.default_content()
                    except:
                        driver.switch_to.default_content()
                        logger.warning(f"Could not switch to iframe {i}")
            
            # If we found the search input, proceed with the search
            if search_input:
                try:
                    # Clear the input and enter "kuala lumpur"
                    search_input.clear()
                    search_input.send_keys("kuala lumpur")
                    logger.info("Entered 'kuala lumpur' in the search input")
                    
                    # Look for the search button using multiple strategies
                    search_button = None
                    button_strategies = [
                        (By.ID, "searchButton"),
                        (By.XPATH, "//button[contains(text(), 'Search')]"),
                        (By.XPATH, "//button[contains(@class, 'search')]"),
                        (By.CSS_SELECTOR, "button[type='submit']"),
                        (By.TAG_NAME, "button")
                    ]
                    
                    for strategy in button_strategies:
                        try:
                            elements = driver.find_elements(strategy[0], strategy[1])
                            if elements:
                                for element in elements:
                                    if element.is_displayed():
                                        search_button = element
                                        logger.info(f"Found visible search button using strategy {strategy}")
                                        break
                            if search_button:
                                break
                        except:
                            pass
                    
                    if search_button:
                        # Click the search button
                        search_button.click()
                        logger.info("Clicked the search button")
                        
                        # Wait for results to load
                        time.sleep(5)
                        
                        # Take screenshot after search
                        driver.save_screenshot("debug/after_search.png")
                        logger.info("Saved screenshot after search")
                        
                        # Save page source after search
                        with open("debug/after_search.html", "w", encoding="utf-8") as f:
                            f.write(driver.page_source)
                        logger.info("Saved page source after search")
                        
                        # Try to identify the results container
                        result_strategies = [
                            (By.CLASS_NAME, "results-list"),
                            (By.CLASS_NAME, "store-list"),
                            (By.CLASS_NAME, "location-list"),
                            (By.XPATH, "//div[contains(@class, 'results')]"),
                            (By.XPATH, "//div[contains(@class, 'store')]"),
                            (By.XPATH, "//div[contains(@class, 'location')]")
                        ]
                        
                        results_container = None
                        for strategy in result_strategies:
                            try:
                                elements = driver.find_elements(strategy[0], strategy[1])
                                if elements and elements[0].is_displayed():
                                    results_container = elements[0]
                                    logger.info(f"Found results container using strategy {strategy}")
                                    break
                            except:
                                pass
                        
                        if results_container:
                            # Extract outlets from the results
                            self._extract_outlets_from_results(driver, results_container)
                        else:
                            logger.error("Could not find results container")
                            # Try a more generic approach to find outlet information
                            self._extract_outlets_generic(driver)
                    else:
                        logger.error("Could not find search button")
                        # Try a more generic approach
                        search_input.send_keys("\n")  # Try pressing Enter
                        time.sleep(5)
                        self._extract_outlets_generic(driver)
                except Exception as e:
                    logger.error(f"Error during search: {str(e)}")
                    # Try a more generic approach
                    self._extract_outlets_generic(driver)
            else:
                logger.error("Could not find search input")
                # Try a more generic approach
                self._extract_outlets_generic(driver)
            
            logger.info(f"Scraping completed. Total outlets scraped: {len(self.outlets)}")
            return self.outlets
            
        except Exception as e:
            logger.error(f"An error occurred during scraping: {str(e)}")
            return []
            
        finally:
            driver.quit()
            logger.info("WebDriver closed")
    
    def _extract_outlets_from_results(self, driver, results_container):
        """Extract outlet information from the results container"""
        logger.info("Extracting outlets from results container")
        
        # Try to find individual outlet elements
        outlet_elements = []
        outlet_strategies = [
            (By.CLASS_NAME, "results-list-item"),
            (By.CLASS_NAME, "store-item"),
            (By.CLASS_NAME, "location-item"),
            (By.XPATH, "//div[contains(@class, 'item')]"),
            (By.TAG_NAME, "li"),
            (By.TAG_NAME, "div")
        ]
        
        for strategy in outlet_strategies:
            try:
                elements = results_container.find_elements(strategy[0], strategy[1])
                if elements:
                    outlet_elements = elements
                    logger.info(f"Found {len(elements)} outlet elements using strategy {strategy}")
                    break
            except:
                pass
        
        if not outlet_elements:
            logger.warning("Could not find outlet elements, trying with the entire page")
            # If we couldn't find specific outlet elements, try to extract information from the entire page
            self._extract_outlets_generic(driver)
            return
        
        # Process each outlet element
        for i, outlet in enumerate(outlet_elements):
            try:
                # Save outlet HTML for debugging
                with open(f"debug/outlet_{i}.html", "w", encoding="utf-8") as f:
                    f.write(outlet.get_attribute('outerHTML'))
                
                # Extract outlet information using multiple strategies
                name = self._extract_text(outlet, [
                    (By.CLASS_NAME, "location-name"),
                    (By.CLASS_NAME, "store-name"),
                    (By.TAG_NAME, "h3"),
                    (By.TAG_NAME, "h4")
                ])
                
                address = self._extract_text(outlet, [
                    (By.CLASS_NAME, "address-line"),
                    (By.CLASS_NAME, "store-address"),
                    (By.XPATH, "//div[contains(@class, 'address')]"),
                    (By.TAG_NAME, "address")
                ])
                
                hours = self._extract_text(outlet, [
                    (By.XPATH, "//div[contains(text(), 'Opening Hours')]"),
                    (By.XPATH, "//div[contains(text(), 'Hours')]"),
                    (By.XPATH, "//span[contains(text(), 'Opening Hours')]"),
                    (By.XPATH, "//span[contains(text(), 'Hours')]")
                ])
                
                # Extract Waze link
                waze_link = ""
                link_elements = outlet.find_elements(By.TAG_NAME, "a")
                for link in link_elements:
                    href = link.get_attribute("href")
                    if href and "waze" in href.lower():
                        waze_link = href
                        break
                
                # Only add the outlet if we at least have a name or address
                if name or address:
                    self.outlets.append({
                        "name": name,
                        "address": address,
                        "operating_hours": hours,
                        "waze_link": waze_link
                    })
                    logger.info(f"Added outlet: {name or 'Unknown'}")
            except Exception as e:
                logger.error(f"Error extracting outlet {i}: {str(e)}")
    
    def _extract_outlets_generic(self, driver):
        """Extract outlet information using a more generic approach"""
        logger.info("Trying to extract outlets using generic approach")
        
        # Save the page source
        with open("debug/generic_extraction.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        # Use BeautifulSoup for more flexible parsing
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Look for common patterns in store locators
        
        # Strategy 1: Look for elements with "store" or "location" in class
        store_elements = soup.find_all(class_=lambda c: c and ('store' in c.lower() or 'location' in c.lower()))
        logger.info(f"Found {len(store_elements)} elements with 'store' or 'location' in class")
        
        # Strategy 2: Look for address elements
        address_elements = soup.find_all(['address', 'div'], class_=lambda c: c and 'address' in c.lower())
        logger.info(f"Found {len(address_elements)} address elements")
        
        # Strategy 3: Look for h3/h4 elements that might be store names
        name_elements = soup.find_all(['h3', 'h4'])
        logger.info(f"Found {len(name_elements)} h3/h4 elements")
        
        # Strategy 4: Look for a elements with waze links
        waze_links = soup.find_all('a', href=lambda h: h and 'waze' in h.lower())
        logger.info(f"Found {len(waze_links)} Waze links")
        
        # Try to pair names with addresses
        if name_elements and address_elements and len(name_elements) == len(address_elements):
            logger.info("Matching names with addresses based on position")
            for i in range(len(name_elements)):
                self.outlets.append({
                    "name": name_elements[i].get_text(strip=True),
                    "address": address_elements[i].get_text(strip=True),
                    "operating_hours": "",
                    "waze_link": ""
                })
        
        # If we still haven't found any outlets, try to extract from Waze links
        if not self.outlets and waze_links:
            logger.info("Extracting outlets from Waze links")
            for link in waze_links:
                # Try to find a parent element that might contain the outlet info
                parent = link.find_parent(['div', 'li'])
                if parent:
                    name = ""
                    address = ""
                    hours = ""
                    
                    # Look for name
                    name_elem = parent.find(['h3', 'h4', 'strong'])
                    if name_elem:
                        name = name_elem.get_text(strip=True)
                    
                    # Look for address
                    address_elem = parent.find(['address', 'div'], class_=lambda c: c and 'address' in c.lower())
                    if address_elem:
                        address = address_elem.get_text(strip=True)
                    elif name:
                        # If we found a name but no explicit address, use the remaining text as address
                        remaining_text = parent.get_text(strip=True).replace(name, '', 1)
                        address = remaining_text
                    
                    # Only add if we have at least some information
                    if name or address:
                        self.outlets.append({
                            "name": name,
                            "address": address,
                            "operating_hours": hours,
                            "waze_link": link.get('href', '')
                        })
        
        logger.info(f"Generic extraction found {len(self.outlets)} outlets")
    
    def _extract_text(self, element, strategies):
        """Extract text from an element using multiple strategies"""
        for strategy in strategies:
            try:
                elements = element.find_elements(strategy[0], strategy[1])
                if elements and elements[0].is_displayed():
                    return elements[0].text.strip()
            except:
                pass
        return ""