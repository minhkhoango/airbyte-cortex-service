# Stage 1: Build stage with build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VENV_IN_PROJECT=1

# Install poetry
RUN pip install poetry
RUN poetry config virtualenvs.in-project true

# Copy only dependency-defining files
COPY poetry.lock pyproject.toml ./

# Install dependencies into a virtual environment
RUN poetry install --no-root --only=main

# Create cache directory and pre-download the Hugging Face model
RUN mkdir -p /app/.cache/huggingface
ENV HF_HOME=/app/.cache/huggingface
RUN poetry run python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Stage 2: Final production stage
FROM python:3.11-slim
WORKDIR /app

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app

# Create NLTK data directory and set permissions
RUN mkdir -p /app/nltk_data && chown -R app:app /app/nltk_data

# Create Hugging Face cache directory with proper permissions
RUN mkdir -p /app/.cache/huggingface && chown -R app:app /app/.cache

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv
# Copy the application code
COPY ./cortex_service ./cortex_service
# Copy the pre-downloaded model cache
COPY --from=builder /app/.cache/huggingface /app/.cache/huggingface

# Fix ownership of copied files to match the app user
RUN chown -R app:app /app/.cache/huggingface

USER app

# Make the virtual environment's binaries accessible
ENV PATH="/app/.venv/bin:$PATH"
ENV NLTK_DATA="/app/nltk_data"
ENV HF_HOME="/app/.cache/huggingface"

# Run the application
CMD ["uvicorn", "cortex_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
