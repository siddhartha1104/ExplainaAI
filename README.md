# ExplainaAI with Vector Memory

A Streamlit application that allows users to extract content from various web sources (YouTube videos, Wikipedia articles,Instagram public profiles or any webpage), process it, and interact with it through a chatbot interface with vector memory.

##### Note

- Python 3.11 (used)

## Features

- Extract content from:
  - YouTube video transcripts
  - Wikipedia articles
  - Static webpages using BeautifulSoup
  - Dynamic webpages using Selenium
- Process and summarize content using the Groq LLM API
- Store content chunks in a vector database (ChromaDB)
- Interactive chat interface with vector search for context-aware responses
- Memory of conversation history for better contextual understanding

## Setup

1. Clone the repository

```bash
git clone https://github.com/siddhartha1104/ExplainaAI.git
cd ExplainaAI
```

2. Create envireonment

```bash
conda create -p venv python==3.11 -y
```

3. Activate envireonment

```bash
conda activate venv/
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys

```
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the application

```bash
streamlit run app.py
```

## Usage

1. Enter a URL in the sidebar (YouTube video, Wikipedia article, or any webpage)
2. Select the appropriate scraping method:
   - Auto: Tries dynamic first, then static
   - Static only: Uses BeautifulSoup
   - Dynamic only: Uses Selenium
3. Click "Process URL" to extract and analyze the content
4. Once processing is complete, you can ask questions about the content in the chat interface

## Project Structure

```
/ExplainaAI/
├── app.py                    # Main Streamlit application
├── .env                      # Environment variables (not tracked in git)
├── .gitignore                # Git ignore file
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
├── /chroma_db/               # Directory for ChromaDB persistence
├── /utils/
│   ├── __init__.py
│   ├── session_state.py      # Session state management
│   ├── text_processing.py    # Text processing utilities
│   └── ui_helpers.py         # UI helper functions
├── /services/
│   ├── __init__.py
│   ├── llm_service.py        # LLM API interactions
│   ├── vector_db.py          # Vector database operations
│   └── web_scraping/
│       ├── __init__.py
│       ├── scraper_base.py   # Base scraper class
│       ├── youtube.py        # YouTube content extraction
│       ├── wikipedia.py      # Wikipedia content extraction
│       ├── static_scraper.py # Static webpage scraping
│       └── dynamic_scraper.py # Dynamic webpage scraping
└── /prompts/
    ├── __init__.py
    └── prompt_templates.py   # All prompt templates
```

## Dependencies

- streamlit: Web application framework
- python-dotenv: Environment variable management
- requests: HTTP requests
- youtube-transcript-api: Extract YouTube video transcripts
- wikipedia-api: Access Wikipedia content
- beautifulsoup4: HTML parsing for static webpages
- chromadb: Vector database for storing content chunks
- selenium: Dynamic webpage scraping
- webdriver-manager: WebDriver management for Selenium

## License

MIT

## Contact

mail@siddharthapathak.com.np
