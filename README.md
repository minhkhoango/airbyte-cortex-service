# Airbyte Cortex Service

[![CI Pipeline](https://github.com/<your-username>/airbyte-cortex-service/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/airbyte-cortex-service/actions/workflows/ci.yml)

A production-grade microservice for intelligent, in-flight pre-processing of unstructured data, making it AI-ready for RAG pipelines in Airbyte.

## Overview

Airbyte is a leader in data movement, but creating production-grade RAG pipelines requires more than just moving data. It requires sophisticated, in-flight transformation of unstructured data into semantically coherent chunks.

The Cortex service solves this "last-mile" problem by providing a robust, configurable API for intelligent chunking and semantic validation, designed to be integrated directly into the Airbyte data flow.

## ✨ Features

-   **Configurable Chunking:** Choose between multiple chunking strategies (`paragraph`, `fixed_size`) via the API.
-   **Semantic Validation:** Each chunk is returned with a cosine similarity score to its next sibling, providing a quantitative measure of contextual coherence.
-   **Production Ready:** Secure API key authentication, structured JSON logging, and Prometheus metrics endpoint (`/metrics`) out of the box.
-   **Containerized:** Packaged with Docker for easy, reproducible deployments.

## 🚀 Getting Started

### Prerequisites

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Set Up Environment

Clone the repository and create a `.env` file from the example:

```bash
git clone [https://github.com/](https://github.com/)<your-username>/airbyte-cortex-service.git
cd airbyte-cortex-service
cp .env.example .env
```

### 2. Run the Service

Launch the service with a single command:

```bash
docker-compose up --build
```

The API will be available at `http://127.0.0.1:8000`. You can see the OpenAPI documentation at `http://127.0.0.1:8000/docs`.

### ⚙️ API Reference

The primary endpoint is `/api/v1/sync`. All requests must include the `X-API-Key` header.

Example `curl` Request:

```bash
curl -X POST "http://localhost:8000/api/v1/sync" \
-H "Content-Type: application/json" \
-H "X-API-Key: your-secret-key-here" \
-d '{
  "document_id": "doc-xyz-789",
  "content": "This is the first paragraph.\n\nThis is the second.",
  "metadata": { "source": "s3-bucket" },
  "chunking_strategy": {
    "name": "paragraph",
    "params": { "min_chunk_size": 10 }
  }
}'
```# Test comment
