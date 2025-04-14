# services/web_scraping/dynamic_scraper.py
import streamlit as st
import time
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from services.web_scraping.scraper_base import BaseScraper

class DynamicWebpageScraper(BaseScraper):
    """Scraper class for extracting content from dynamic webpages using Selenium"""
    
    def extract_content(self, url, wait_time=5):
        """Extract content from a dynamic webpage using Selenium"""
        driver = None
        try:
            with st.spinner("Loading dynamic content with Selenium..."):
                # Configure Chrome options
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                
                # Set up the driver
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Navigate to the URL
                driver.get(url)
                
                # Wait for the dynamic content to load
                time.sleep(wait_time)
                
                # Extract the page title
                title = driver.title
                
                # Get the fully rendered page source
                page_source = driver.page_source
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Remove script, style elements and comments
                for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
                    element.decompose()
                    
                # Extract text from paragraphs, headings, and lists
                content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
                
                content = []
                for element in content_elements:
                    text = element.get_text(strip=True)
                    if text and len(text) > 20:  # Filter out very short texts
                        content.append(text)
                        
                # Join all paragraphs with newlines
                full_text = "\n\n".join(content)
                
                # Get the webpage favicon or domain icon
                domain = urllib.parse.urlparse(url).netloc
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=64"
                
                # Close the driver
                driver.quit()
                
                return full_text, title, favicon_url
        except Exception as e:
            if driver:
                driver.quit()
            return self.handle_error(e, "Error extracting dynamic webpage content")

# Function wrapper for easy usage
def extract_dynamic_webpage_content(url, wait_time=5):
    """Extract content, title, and favicon from a dynamic webpage"""
    scraper = DynamicWebpageScraper()
    return scraper.extract_content(url, wait_time)