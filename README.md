# String Analyzer API v2

A FastAPI-based string analysis service with natural language query filtering and Docker support.

## Features

- 🔍 **String Analysis**: Automatic analysis of string properties (length, palindrome detection, character frequency, etc.)
- 🧠 **NLP Filtering**: Query strings using natural language (e.g., "palindromic strings longer than 5 characters")
- 🔐 **SHA-256 Hashing**: Unique identification for each string
- 💾 **Persistent Storage**: JSON-based database with data persistence
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- ✅ **Fully Tested**: Comprehensive test suite with pytest

## Quick Start

### Using Docker (Recommended)

```bash
# Build the image
docker build -t string-analyzer-ii .

# Run the container
docker run -d --name string-analyzer \
  -p 8000:8000 \
  -v $(pwd)/data:/code/data \
  string-analyzer-ii

# Access the API
curl http://localhost:8000/
```

### Using Docker Compose

```bash
# Start the service
docker-compose up -d

# Stop the service
docker-compose down
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the application
uvicorn app.main:app --reload

# Run tests
pytest
```

## API Endpoints

### Create String
```bash
POST /strings
Body: {"value": "racecar"}
```

### Get String
```bash
GET /strings/{string_value}
```

### List All Strings
```bash
GET /strings
Query params: is_palindrome, min_length, max_length, word_count, contains_character
```

### Natural Language Filter
```bash
GET /strings/filter-by-natural-language?query=palindromic strings longer than 5
```

### Delete String
```bash
DELETE /strings/{string_value}
```

## Example Usage

```bash
# Create strings
curl -X POST http://localhost:8000/strings -H "Content-Type: application/json" -d '{"value": "racecar"}'
curl -X POST http://localhost:8000/strings -H "Content-Type: application/json" -d '{"value": "hello world"}'

# Filter palindromes
curl "http://localhost:8000/strings?is_palindrome=true"

# Natural language query
curl "http://localhost:8000/strings/filter-by-natural-language?query=palindromic%20strings"

# Get specific string
curl http://localhost:8000/strings/racecar
```

## Project Structure

```
string-analyzer-v2/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── models.py         # Pydantic models
│   ├── database.py       # JSON database logic
│   ├── logic.py          # String analysis logic
│   ├── nlp.py            # Natural language processing
│   ├── filtering.py      # Filter application logic
│   └── test_main.py      # Test suite
├── data/                 # Database storage (gitignored)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Technologies Used

- **FastAPI**: Modern Python web framework
- **spaCy**: Natural language processing
- **Pydantic**: Data validation
- **Docker**: Containerization
- **pytest**: Testing framework

## Development

```bash
# Run tests
pytest

# Run with auto-reload
uvicorn app.main:app --reload

# View logs (Docker)
docker logs -f string-analyzer
```

## License

MIT License

## Author

Saint - [GitHub Profile](https://github.com/aluyapeter)