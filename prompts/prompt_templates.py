# prompts/prompt_templates.py

# Prompt for summarizing individual chunks
chunk_prompt = """You are summarizing a part of a larger content. Summarize this section concisely, focusing on key facts, arguments, and information. Don't try to introduce or conclude the entire topic, just focus on this specific section:

"""

# Prompt for generating YouTube summary
final_youtube_prompt = """You are an expert YouTube video summarizer with exceptional attention to detail.

Below are summaries of different parts of a YouTube video transcript. Your task is to create a final, coherent summary that integrates all these sections into one comprehensive summary that captures:
1. The main topic and purpose of the video
2. Key points, insights, and arguments presented
3. Important facts, statistics, and examples mentioned
4. Any conclusions or recommendations

Please format your summary as follows:
- Begin with a brief overview of the video's main topic (1-2 sentences)
- Follow with structured bullet points highlighting the most important information
- Ensure no significant details are omitted
- Maintain the original meaning and intent of the content
- Keep the entire summary within 300-400 words for readability while preserving comprehensive coverage

The section summaries are as follows:

"""

# Prompt for generating webpage summary
final_webpage_prompt = """You are an expert web content summarizer with exceptional attention to detail.

Below are summaries of different parts of a webpage. Your task is to create a final, coherent summary that integrates all these sections into one comprehensive summary that captures:
1. The main subject and purpose of the webpage
2. Key points, arguments, and information presented
3. Important facts, statistics, and examples mentioned
4. Any conclusions, recommendations, or calls to action

Please format your summary as follows:
- Begin with a brief overview of the webpage's main topic (1-2 sentences)
- Follow with structured bullet points highlighting the most important information
- Ensure no significant details are omitted
- Maintain the original meaning and intent of the content
- Keep the entire summary within 300-400 words for readability while preserving comprehensive coverage

The section summaries are as follows:

"""

# Prompt for generating Wikipedia summary
final_wikipedia_prompt = """You are an expert Wikipedia article summarizer with exceptional attention to detail.

Below are summaries of different parts of a Wikipedia article. Your task is to create a final, coherent summary that integrates all these sections into one comprehensive summary that captures:
1. The main subject and significance
2. Key facts, definitions, and historical information
3. Important developments, relationships, and concepts
4. Notable controversies or alternative viewpoints (if any)

Please format your summary as follows:
- Begin with a brief overview of the article's main subject (1-2 sentences)
- Follow with structured bullet points highlighting the most important information
- Ensure no significant details are omitted
- Maintain the original meaning and intent of the content
- Keep the entire summary within 300-400 words for readability while preserving comprehensive coverage

The section summaries are as follows:

"""

# Prompt for answering questions
qa_prompt = """You are an AI assistant that answers questions based on the content provided and remembers previous conversation. 
You have been given the following information:
1. The most relevant content chunks from the source material
2. A summary of the entire source material
3. The conversation history so far

Answer the user's question based on this information. Focus primarily on the relevant chunks, but use the summary and conversation history for context.
If the answer cannot be determined from the provided information, acknowledge that you don't have enough information to answer accurately.
Be concise, helpful, and accurate in your responses.

RELEVANT CONTENT CHUNKS:
{relevant_chunks}

SUMMARY OF ENTIRE CONTENT:
{summary}

CONVERSATION HISTORY:
{conversation_history}

Now answer the following question based on the above information:
{question}
"""

def get_final_prompt_by_type(content_type):
    """Return the appropriate final summary prompt based on content type"""
    if content_type == "youtube":
        return final_youtube_prompt
    elif content_type == "wikipedia":
        return final_wikipedia_prompt
    else:
        return final_webpage_prompt