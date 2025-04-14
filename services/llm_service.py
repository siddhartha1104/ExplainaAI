# services/llm_service.py
import os
import time
import requests
import json
import streamlit as st

from services.vector_db import store_chunks_in_vector_db, query_vector_db, get_or_create_collection
from prompts.prompt_templates import qa_prompt, chunk_prompt, get_final_prompt_by_type
from utils.text_processing import split_into_chunks, format_conversation_history

# Configure Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Generate content using Groq API
def generate_groq_content(content_text, prompt, model="llama3-70b-8192"):
    """Generate content using the Groq API"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert content summarizer that extracts comprehensive yet concise information from provided text."
            },
            {
                "role": "user",
                "content": prompt + content_text
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 429:  # Rate limit error
            st.warning("Rate limit reached. Waiting before retrying...")
            time.sleep(5)  # Wait 5 seconds before retrying
            return generate_groq_content(content_text, prompt, model)  # Retry
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Error making API call: {str(e)}"

# Process content in chunks and add to vector database
def process_large_content(content, content_type, source_url, collection_name):
    """Process large content by chunking, summarizing, and storing in vector DB"""
    with st.status("Processing content in chunks...") as status:        
        # Split content into chunks for summarization and for vector DB
        summary_chunks = split_into_chunks(content, max_chunk_size=4000)
        vector_chunks = split_into_chunks(content, max_chunk_size=1000, overlap=100)
        
        status.update(label=f"Split into {len(summary_chunks)} summary chunks and {len(vector_chunks)} vector chunks")
        
        # Process each chunk for summary
        chunk_summaries = []
        progress_bar = st.progress(0)
        
        for i, chunk in enumerate(summary_chunks):
            status.update(label=f"Processing summary chunk {i+1}/{len(summary_chunks)}...")
            chunk_summary = generate_groq_content(chunk, chunk_prompt, "llama3-8b-8192")  # Using smaller model for chunks
            chunk_summaries.append(chunk_summary)
            progress_bar.progress((i + 1) / len(summary_chunks))
            # Add a delay to respect rate limits
            time.sleep(1)
        
        # Combine chunk summaries
        combined_summaries = "\n\n--- SECTION SUMMARY " + " ---\n\n--- SECTION SUMMARY ".join(chunk_summaries) + " ---\n\n"
        
        # Generate final summary based on content type
        final_prompt = get_final_prompt_by_type(content_type)
            
        status.update(label="Generating final summary...")
        final_summary = generate_groq_content(combined_summaries, final_prompt, "llama3-70b-8192")
        
        # Store chunks in vector database
        status.update(label="Storing content in vector database...")
        metadata = {
            "source": source_url,
            "title": st.session_state.page_title,
            "type": content_type
        }
        
        # Store in vector database
        vector_db = store_chunks_in_vector_db(vector_chunks, collection_name, metadata)
        st.session_state.vector_db = vector_db
        
        status.update(label="Processing complete!", state="complete")
        
        return final_summary

# Answer questions based on extracted content with vector database search
def answer_question(question):
    """Generate an answer to a question using vector search and LLM"""
    # Get conversation history (excluding the current question and initial system message)
    conversation_history = st.session_state.chat_history[1:] if len(st.session_state.chat_history) > 1 else []
    
    # Format the conversation history
    formatted_history = format_conversation_history(conversation_history)
    
    # Query vector database for relevant chunks
    with st.spinner("Searching relevant content..."):
        if st.session_state.vector_db:
            results = query_vector_db(question, st.session_state.vector_db, n_results=3)
            relevant_chunks = results['documents'][0]
            relevant_chunks_text = "\n\n---\n\n".join(relevant_chunks)
        else:
            # Fallback if vector DB is not available
            relevant_chunks_text = "Vector database not available. Using summary only."
    
    # Prepare the prompt with relevant chunks, summary, conversation history, and question
    formatted_prompt = qa_prompt.format(
        relevant_chunks=relevant_chunks_text,
        summary=st.session_state.summary,
        conversation_history=formatted_history,
        question=question
    )
    
    # Generate answer using Groq API with memory-aware prompt
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant that answers questions based on relevant content and remembers past conversation."
            },
            {
                "role": "user",
                "content": formatted_prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Error making API call: {str(e)}"