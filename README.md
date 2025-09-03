# LLM Knowledge Extractor

An intelligent text analysis application that extracts key insights from text snippets using OpenAI's LLM and NLTK for natural language processing. The application processes text and returns structured analysis including summaries, key topics, sentiment analysis, and keywords.

## Features

- **Text Analysis**: Generate summaries, extract key topics, and analyze sentiment
- **Keyword Extraction**: Extract the most common nouns using NLTK
- **Data Persistence**: Store analysis results in SQLite database
- **Search Functionality**: Search stored analyses by keyword or sentiment
- **RESTful API**: Clean FastAPI endpoints for easy integration

### Example Output

```json
{
  "summary": "The local church serves as a community for Christians and also welcomes non-believers, but it often faces challenges in encouraging both believers to attend and non-believers to join. The text emphasizes the importance of meeting together for mutual support and encouragement among believers.",
  "title": null,
  "key_topics": [
      "community",
      "church attendance",
      "encouragement"
  ],
  "sentiment": "positive",
  "keywords": [
      "community",
      "believers",
      "effort"
  ]
}
```

## Setup and Run Instructions

### Prerequisites

- Python 3.8+
- OpenAI API key

### Local Development

1. **Clone and navigate to the project**:

   ```bash
   cd llm-knowledge-extractor
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:

   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_PATH=knowledge.db
   ```

5. **Run the application**:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Using Docker

1. **Build and run with Docker Compose**:

   ```bash
   docker-compose up --build
   ```

   The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - Health check
- `POST /analyze` - Analyze text (requires `{"text": "your text here"}`)
- `GET /search?keyword=value` - Search by keyword
- `GET /search?sentiment=value` - Search by sentiment

### Running Tests

```bash
pytest
```

## Design Decisions

I structured this application with clear separation of concerns using a modular architecture where database operations, AI services, and business logic are isolated into distinct layers.

- FastAPI was chosen as the web framework due to its excellent async support, automatic API documentation, and strong typing integration with Pydantic for request/response validation.
- The combination of OpenAI's LLM for intelligent text analysis and NLTK for traditional NLP tasks provides both cutting-edge AI capabilities and reliable linguistic processing.
- SQLite serves as the database solution because it requires no external setup while still providing full SQL capabilities and easy deployment, making it ideal for this focused text analysis application.

## Trade-offs

Due to time constraints, several simplifications were made:

- The application uses a single SQLite database file without connection pooling, which limits scalability under high concurrent load.
- Error handling is basic and doesn't include comprehensive retry logic or detailed error categorization that would be essential in production.
- The search functionality only supports exact keyword matching rather than semantic search, and there's no caching layer for repeated analyses of identical text.
- Additionally, the application lacks user authentication, rate limiting, and comprehensive logging that would be required for a production deployment.
