# services/web_scraping/youtube.py
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from services.web_scraping.scraper_base import BaseScraper

class YouTubeScraper(BaseScraper):
    """Scraper class for extracting YouTube video transcripts"""
    
    def extract_content(self, url):
        """Extract transcript from YouTube video URL"""
        try:
            if "youtube.com" in url and "=" in url:
                video_id = url.split("=")[1]
            elif "youtu.be" in url:
                video_id = url.split("/")[-1]
            else:
                return self.handle_error(ValueError("Invalid URL format"), "Invalid YouTube URL format")
                
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = ""
            for i in transcript_text:
                transcript += " " + i["text"]
            return transcript, video_id
        except Exception as e:
            return self.handle_error(e, "Error extracting YouTube transcript")

# Function wrapper for easy usage
def extract_transcript_details(youtube_video_url):
    """Extract transcript and video ID from a YouTube URL"""
    scraper = YouTubeScraper()
    return scraper.extract_content(youtube_video_url)