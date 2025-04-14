# Session state management
# utils/session_state.py
import streamlit as st

def initialize_session_state():
    """Initialize all session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'extracted_content' not in st.session_state:
        st.session_state.extracted_content = ""
    if 'content_source' not in st.session_state:
        st.session_state.content_source = ""
    if 'summary' not in st.session_state:
        st.session_state.summary = ""
    if 'url_processed' not in st.session_state:
        st.session_state.url_processed = False
    if 'url_type' not in st.session_state:
        st.session_state.url_type = None
    if 'page_title' not in st.session_state:
        st.session_state.page_title = ""
    if 'vector_db' not in st.session_state:
        st.session_state.vector_db = None
    if 'collection_name' not in st.session_state:
        st.session_state.collection_name = ""