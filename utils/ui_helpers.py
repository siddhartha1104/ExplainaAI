# UI helper functions
# utils/ui_helpers.py
import streamlit as st

def render_content_source_info():
    """Render information about the content source"""
    st.subheader("Content Source")
    st.write(st.session_state.content_source)
    
    if st.session_state.url_type == "youtube" and "YouTube Video (ID:" in st.session_state.content_source:
        video_id = st.session_state.content_source.split("ID: ")[1].strip(")")
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    elif st.session_state.url_type == "wikipedia":
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/200px-Wikipedia-logo-v2.svg.png", width=100)

def render_chat_history():
    """Display chat history in the UI"""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])