# services/web_scraping/static_scraper.py
import streamlit as st
import requests
import urllib.parse
from bs4 import BeautifulSoup
from services.web_scraping.scraper_base import BaseScraper

class StaticWebpageScraper(BaseScraper):
    """Scraper class for extracting content from static webpages"""
    
    def extract_content(self, url):
        """Extract content from a static webpage using BeautifulSoup"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else "No title found"
            
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
            
            return full_text, title, favicon_url
        except Exception as e:
            return self.handle_error(e, "Error extracting static webpage content")

# Function wrapper for easy usage
def extract_static_webpage_content(url):
    """Extract content, title, and favicon from a static webpage"""
    scraper = StaticWebpageScraper()
    return scraper.extract_content(url)