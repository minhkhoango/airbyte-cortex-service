# Stage 1: Build stage with build dependencies
FROM python:3.11-slim as builder

WORKDIR /app
ENV POETRY_NO_INTERACTION=1

# Install poetry
RUN pip install poetry

# Copy only dependency-defining files
COPY poetry.lock pyproject.toml ./

# Install dependencies into a virtual environment
RUN poetry install --no-root --no-dev

# Stage 2: Final production stage
FROM python:3.11-slim
WORKDIR /app

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app
USER app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /.venv
# Copy the application code
COPY ./cortex_service ./cortex_service

# Make the virtual environment's binaries accessible
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uvicorn", "cortex_service.main:app", "--host", "0.0.0.0", "--port", "8000"]