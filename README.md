# Airbyte Cortex Service

AI-ready data pre-processing service for Airbyte with intelligent document chunking.

## Quick Start

### Prerequisites
- Python 3.11-3.13
- Poetry

### Install & Run

```bash
# Install dependencies
poetry install

# Run the service
poetry run uvicorn cortex_service.main:app --host 0.0.0.0 --port 8000

curl -X POST "http://127.0.0.1:8000/api/v1/sync" \
-H "Content-Type: application/json" \
-H "X-API-Key: cortex-secret-key-do-not-commit" \
-d '{
        "document_id": "123", 
        "content": "hello", 
        "chunking_strategy": {"name": "paragraph"}
    }'
```
http://127.0.0.1:8000/metrics

### API Endpoints

- `GET /health` - Health check
- `POST /api/v1/sync` - Process documents (requires API key)
- `GET /metrics` - Prometheus metrics

### Environment Variables

Create `.env` file:
```env
API_KEY=your_secret_key_here
```

### Docker (Optional)

```bash
docker build -t airbyte-cortex .
docker run -p 8000:8000 airbyte-cortex
```

## Features

- Intelligent document chunking (paragraph-based, fixed-size)
- Semantic similarity validation
- FastAPI with Prometheus metrics
- API key authentication
