# services/web_scraping/scraper_base.py
import streamlit as st

class BaseScraper:
    """Base class for all web scrapers"""
    
    def __init__(self):
        pass
    
    def extract_content(self, url):
        """Extract content from a URL - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement extract_content")
    
    def handle_error(self, error, message="Error extracting content"):
        """Handle errors during content extraction"""
        st.error(f"{message}: {str(error)}")
        return None