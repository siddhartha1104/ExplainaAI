# utils/text_processing.py

# Function to split text into chunks of approximately equal size
def split_into_chunks(text, max_chunk_size=1000, overlap=100):
    """Split text into chunks of approximately max_chunk_size characters with overlap."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        # Add word length plus space
        if current_size + len(word) + 1 > max_chunk_size and current_chunk:
            # If adding this word would exceed the limit, save current chunk and start a new one
            chunk_text = ' '.join(current_chunk)
            chunks.append(chunk_text)
            
            # Create overlap by taking the last N words for the next chunk
            overlap_words = current_chunk[-int(overlap/5):] if overlap > 0 else []
            current_chunk = overlap_words + [word]
            current_size = sum(len(w) + 1 for w in current_chunk)
        else:
            # Add word to current chunk
            current_chunk.append(word)
            current_size += len(word) + 1
            
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))
        
    return chunks

# Function to format conversation history for the prompt
def format_conversation_history(chat_history):
    """Format the conversation history for inclusion in prompts"""
    if not chat_history:
        return "No previous conversation."
    
    formatted_history = ""
    for i, message in enumerate(chat_history):
        role = "User" if message["role"] == "user" else "Assistant"
        formatted_history += f"{role}: {message['content']}\n\n"
    
    return formatted_history