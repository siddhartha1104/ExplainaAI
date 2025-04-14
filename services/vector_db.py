# services/vector_db.py
import streamlit as st
import time
import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB client
@st.cache_resource
def get_chroma_client():
    """Create a persistent client that saves data to disk"""
    client = chromadb.PersistentClient(path="./chroma_db")
    return client

# Use ChromaDB's default embedding function
@st.cache_resource
def get_embedding_function():
    """Get the default embedding function from ChromaDB"""
    default_ef = embedding_functions.DefaultEmbeddingFunction()
    return default_ef

# Create or get vector database collection
def get_or_create_collection(collection_name):
    """Get an existing collection or create a new one"""
    client = get_chroma_client()
    embedding_func = get_embedding_function()
    
    # Try to get existing collection or create new one
    try:
        collection = client.get_collection(name=collection_name, embedding_function=embedding_func)
    except:
        collection = client.create_collection(name=collection_name, embedding_function=embedding_func)
    
    return collection

# Store text chunks in vector database
def store_chunks_in_vector_db(chunks, collection_name, metadata=None):
    """Store text chunks in the vector database"""
    collection = get_or_create_collection(collection_name)
    
    # Clear existing data if any
    try:
        collection.delete(where={"source": metadata.get("source", "unknown")})
    except:
        pass
    
    # Prepare documents, ids, and metadata
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [metadata] * len(chunks) if metadata else [{"chunk_id": i} for i in range(len(chunks))]
    
    # Add documents to collection in batches to avoid timeout
    batch_size = 10
    for i in range(0, len(chunks), batch_size):
        end_idx = min(i + batch_size, len(chunks))
        try:
            collection.add(
                documents=chunks[i:end_idx],
                ids=ids[i:end_idx],
                metadatas=metadatas[i:end_idx]
            )
            time.sleep(0.5)  # Reduced delay since we're not calling external API
        except Exception as e:
            st.error(f"Error adding documents to vector DB: {str(e)}")
            # Try with smaller batch if there's an error
            if end_idx - i > 1:
                for j in range(i, end_idx):
                    try:
                        collection.add(
                            documents=[chunks[j]],
                            ids=[ids[j]],
                            metadatas=[metadatas[j]]
                        )
                        time.sleep(0.5)
                    except Exception as inner_e:
                        st.error(f"Error adding document {j}: {str(inner_e)}")
    
    return collection

# Fetch relevant chunks from vector database
def query_vector_db(query, collection, n_results=5):
    """Query the vector database to find relevant content chunks"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    return results