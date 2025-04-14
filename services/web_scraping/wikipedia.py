# services/web_scraping/wikipedia.py
import streamlit as st
import re
import wikipediaapi
from services.web_scraping.scraper_base import BaseScraper

class WikipediaScraper(BaseScraper):
    """Scraper class for extracting Wikipedia article content"""
    
    def extract_content(self, url):
        """Extract content from Wikipedia URL"""
        try:
            # Extract the title from the URL
            title_match = re.search(r'wikipedia\.org/wiki/(.+)', url)
            if not title_match:
                return self.handle_error(ValueError("Invalid URL format"), 
                                        "Invalid Wikipedia URL. Please provide a link in the format: https://en.wikipedia.org/wiki/Article_Title")
                
            title = title_match.group(1)
            title = title.replace('_', ' ')
            
            # Initialize Wikipedia API
            wiki_wiki = wikipediaapi.Wikipedia('WikiSummarizerApp/1.0', 'en')
            page = wiki_wiki.page(title)
            
            if not page.exists():
                return self.handle_error(ValueError(f"Page {title} does not exist"), 
                                        f"Wikipedia page '{title}' does not exist or could not be found.")
                
            return page.text, title
        except Exception as e:
            return self.handle_error(e, "Error extracting Wikipedia content")

# Function wrapper for easy usage
def extract_wikipedia_content(wikipedia_url):
    """Extract content and title from a Wikipedia URL"""
    scraper = WikipediaScraper()
    return scraper.extract_content(wikipedia_url)