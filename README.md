# Airbyte Cortex Service

[![CI Pipeline](https://github.com/minhkhoango/airbyte-cortex-service/actions/workflows/ci.yml/badge.svg)](https://github.com/minhkhoango/airbyte-cortex-service/actions/workflows/ci.yml)

A production-grade microservice for intelligent, in-flight pre-processing of unstructured data, making it AI-ready for RAG pipelines in Airbyte.

## Overview

Airbyte is a leader in data movement, but creating production-grade RAG pipelines requires more than just moving data. It requires sophisticated, in-flight transformation of unstructured data into semantically coherent chunks.

The Cortex service solves this "last-mile" problem by providing a robust, configurable API for intelligent chunking and semantic validation, designed to be integrated directly into the Airbyte data flow.

## Business Impact

- **ACV Expansion:** Enables 25-50% premium pricing on enterprise tiers through advanced AI-ready data transformation capabilities
- **TAM Capture:** Positions Airbyte to capture 2-4% of the $14.7B AI-ready data preparation market
- **New Revenue Streams:** Unlocks consumption-based pricing models for data transformation, similar to dbt Labs' successful monetization strategy

## ✨ Features

- **Configurable Chunking:** Multiple chunking strategies (`paragraph`, `fixed_size`) via API configuration
- **Semantic Validation:** Cosine similarity scoring between chunks for contextual coherence measurement
- **Production Ready:** API key authentication, structured logging, and Prometheus metrics endpoint (`/metrics`)
- **Containerized:** Docker packaging for reproducible deployments
- **Pre-downloaded Models:** Hugging Face models are downloaded during build time for faster startup

## Architecture

Cortex is a stateless, containerized microservice designed as an in-flight transformation step within the Airbyte data pipeline. It processes unstructured content and returns semantically coherent chunks optimized for RAG applications.

```mermaid
sequenceDiagram
    participant Source Worker
    participant Transformation Worker as T_Worker
    participant Cortex Service as Cortex
    participant Destination Worker

    Source Worker-->>T_Worker: Stream of AirbyteRecordMessages
    loop For Each Record
        T_Worker->>Cortex: POST /sync (document content)
        Cortex-->>T_Worker: 200 OK (chunked data)
    end
    T_Worker-->>Destination Worker: Stream of chunked AirbyteRecordMessages
```

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Set Up Environment

Clone the repository and create a `.env` file:

```bash
git clone https://github.com/minhkhoango/airbyte-cortex-service.git
cd airbyte-cortex-service
cp .env.example .env
```

### 2. Configure Environment Variables

Edit the `.env` file with your configuration:

```bash
# Required: Set your API key
CORTEX_API_KEY=your-secret-api-key-here

# Optional: Hugging Face token (only needed for private models)
# HUGGINGFACE_HUB_TOKEN=your-hf-token-here

# Optional: Custom model (defaults to all-MiniLM-L6-v2)
# SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
```

**Note:** The default model `all-MiniLM-L6-v2` is a public model that doesn't require authentication. You only need a Hugging Face token if you plan to use private models.

### 3. Run the Service

Launch the service:

```bash
docker-compose up --build
```

The API will be available at `http://127.0.0.1:8000`. View the OpenAPI documentation at `http://127.0.0.1:8000/docs`.

### 🔧 Troubleshooting

#### Docker Build Issues

If you encounter Docker build issues:

1. **Clean Docker system:**
   ```bash
   docker system prune -f
   docker-compose down --volumes --remove-orphans
   ```

2. **Rebuild from scratch:**
   ```bash
   docker-compose up --build --force-recreate
   ```

#### Model Download Issues

The service pre-downloads the Hugging Face model during the Docker build process. If you encounter issues:

1. **Check internet connectivity** during build
2. **For private models**, ensure your `HUGGINGFACE_HUB_TOKEN` is set in the `.env` file
3. **For rate limiting**, the build may take longer but should complete successfully

#### Performance Optimization

For production deployments:

1. **Use a model cache volume** to persist downloaded models:
   ```yaml
   # Add to docker-compose.yml
   volumes:
     - model_cache:/root/.cache/huggingface
   ```

2. **Consider using a smaller model** for faster inference:
   ```bash
   # In .env file
   SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L12-v2
   ```

### ⚙️ API Reference

The primary endpoint is `/api/v1/sync`. All requests must include the `X-API-Key` header.

Example `curl` Request:

```bash
curl -X POST "http://localhost:8000/api/v1/sync" \
-H "Content-Type: application/json" \
-H "X-API-Key: test-api-key-123" \
-d '{
  "document_id": "doc-xyz-789",
  "content": "This is the first paragraph.\n\nThis is the second.",
  "metadata": { "source": "s3-bucket" },
  "chunking_strategy": {
    "name": "paragraph",
    "params": { "min_chunk_size": 10 }
  }
}'
```

### 📊 Monitoring

The service exposes Prometheus metrics at `/metrics` for monitoring:

- Request duration and count
- Error rates
- Model inference metrics

### 🔒 Security

- API key authentication required for all endpoints
- Non-root user in Docker container
- Structured logging for audit trails
