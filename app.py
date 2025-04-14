# Main Streamlit application

# app.py
import streamlit as st
import os
import time
import re

# Import local modules
from utils.session_state import initialize_session_state
from utils.ui_helpers import render_content_source_info, render_chat_history
from services.web_scraping.youtube import extract_transcript_details
from services.web_scraping.wikipedia import extract_wikipedia_content
from services.web_scraping.static_scraper import extract_static_webpage_content
from services.web_scraping.dynamic_scraper import extract_dynamic_webpage_content
from services.llm_service import answer_question, process_large_content
from services.vector_db import get_or_create_collection
from prompts.prompt_templates import get_final_prompt_by_type

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Check for required API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize session state
initialize_session_state()

# Determine URL type
def get_url_type(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "wikipedia.org" in url:
        return "wikipedia"
    else:
        return "webpage"

# Process URL and extract content
def process_url(url, scraping_method, wait_time=5):
    url_type = get_url_type(url)
    st.session_state.url_type = url_type
    
    with st.status(f"Processing {url_type} content...") as status:
        if url_type == "youtube":
            # Process YouTube URL
            content, video_id = extract_transcript_details(url)
            if content and video_id:
                st.session_state.content_source = f"YouTube Video (ID: {video_id})"
                st.session_state.extracted_content = content
                st.session_state.page_title = "YouTube Video"
                status.update(label="YouTube transcript extracted", state="complete")
                return True, url
        elif url_type == "wikipedia":
            # Process Wikipedia URL
            content, title = extract_wikipedia_content(url)
            if content:
                st.session_state.content_source = f"Wikipedia Article: {title}"
                st.session_state.extracted_content = content
                st.session_state.page_title = title
                status.update(label="Wikipedia content extracted", state="complete")
                return True, url
        else:
            # Process general webpage based on scraping method
            if scraping_method == "Auto (Try dynamic first, then static)":
                content, page_title, favicon_url = extract_dynamic_webpage_content(url, wait_time)
                if not content:  # If dynamic extraction failed, try static
                    status.update(label="Dynamic extraction failed, trying static method...")
                    content, page_title, favicon_url = extract_static_webpage_content(url)
            elif scraping_method == "Dynamic only (Selenium)":
                content, page_title, favicon_url = extract_dynamic_webpage_content(url, wait_time)
            else:  # Static only
                content, page_title, favicon_url = extract_static_webpage_content(url)
                
            if content:
                st.session_state.content_source = f"Webpage: {page_title}"
                st.session_state.extracted_content = content
                st.session_state.page_title = page_title
                status.update(label=f"Content extracted from {page_title}", state="complete")
                return True, url
        
        status.update(label="Failed to extract content", state="error")
        return False, url

# Generate summary of extracted content and store in vector database
def summarize_content(source_url):
    content = st.session_state.extracted_content
    url_type = st.session_state.url_type
    
    # Generate a collection name based on the content source
    collection_name = re.sub(r'[^a-zA-Z0-9_]', '_', st.session_state.page_title)[:40]
    # Ensure it starts and ends with alphanumeric characters
    collection_name = re.sub(r'^[._-]+', '', collection_name)
    collection_name = re.sub(r'[._-]+$', '', collection_name) 

    if len(collection_name) < 3:
        collection_name = f"content_{collection_name}"
    
    st.session_state.collection_name = collection_name
    
    # Process content, create summary, and store in vector database
    summary = process_large_content(content, url_type, source_url, collection_name)
    
    st.session_state.summary = summary
    return summary

# Function to clear conversation history
def clear_conversation():
    # Preserve the first message (system introduction)
    if len(st.session_state.chat_history) > 0:
        initial_message = st.session_state.chat_history[0]
        st.session_state.chat_history = [initial_message]
    else:
        st.session_state.chat_history = []
    st.success("Conversation history cleared!")

# Main Streamlit app
st.title("Explaina AI with Vector Memory")
st.write("Enter any URL to extract content and chat with Explaina AI. The Explaina AI will remember your conversation and use vector search to find relevant content!")

# Sidebar for URL input and processing
with st.sidebar:
    st.markdown("""
    ### Developed by: 
    [**Siddhartha Pathak**](https://www.siddharthapathak.com.np)
    """, unsafe_allow_html=True)

    st.divider()

    st.header("Content Source")
    url = st.text_input("Enter URL (YouTube, Wikipedia, or any webpage):")
    
    # Option for scraping method
    scraping_method = st.radio(
        "Select scraping method:",
        ["Auto (Try dynamic first, then static)", "Static only (BeautifulSoup)", "Dynamic only (Selenium)"]
    )
    
    # Dynamic scraping settings
    if scraping_method != "Static only (BeautifulSoup)":
        wait_time = st.slider("Wait time for dynamic content (seconds)", 1, 20, 5)
    else:
        wait_time = 5
    
    # Check for API keys before processing
    if not GROQ_API_KEY:
        st.warning("Missing GROQ_API_KEY for LLM processing\nPlease set this in your .env file")
    
    if st.button("Process URL"):
        if GROQ_API_KEY:
            st.session_state.url_processed = False
            st.session_state.chat_history = []
            
            # Process the URL and extract content
            success, source_url = process_url(url, scraping_method, wait_time)
            
            if success:
                # Summarize content and store in vector database
                summary = summarize_content(source_url)
                st.session_state.url_processed = True
                
                # Add system message to chat history
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": f"I've analyzed the content from {st.session_state.content_source}. Here's a summary:\n\n{summary}\n\nYou can now ask me questions about this content! I'll use vector search to find the most relevant information."
                })
        else:
            st.error("Missing API key. Please set GROQ_API_KEY in your .env file")
    
    if st.session_state.url_processed:
        st.success(f"Content processed: {st.session_state.page_title}")
        
        # Display content source info
        render_content_source_info()
        
        # Collection info
        st.subheader("Vector Database")
        st.write(f"Collection: {st.session_state.collection_name}")

        # Button to view the full extracted content
        if st.button("View Full Extracted Content"):
            st.text_area("Raw Extracted Content", st.session_state.extracted_content, height=300)
            
        # Button to view the summary
        if st.button("View Summary"):
            st.text_area("Content Summary", st.session_state.summary, height=300)
        
        # Button to clear conversation history
        if st.button("Clear Conversation History"):
            clear_conversation()

# Chat interface
st.divider()
st.subheader("Chat with the Content")

# Display chat history
render_chat_history()

# Chat input
if st.session_state.url_processed:
    user_question = st.chat_input("Ask a question about the content...")
    
    if user_question:
        # Add user question to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        # Display user question
        with st.chat_message("user"):
            st.write(user_question)
        
        # Generate and display answer using vector search
        with st.chat_message("assistant"):
            with st.spinner("Searching and thinking..."):
                answer = answer_question(user_question)
                st.write(answer)
                
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
else:
    st.info("Please enter a URL first to start chatting about its content.")

if __name__ == "__main__":
    # This will run when the script is executed directly
    pass