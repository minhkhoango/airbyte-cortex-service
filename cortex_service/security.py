# Pylance strict mode
import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

# Load environment variables from .env file
load_dotenv()

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

# For testing purposes, provide a default key if none is set
CORTEX_API_KEY: str | None = os.getenv("CORTEX_API_KEY", "test-key-if-not-set")


def get_api_key(api_key_header: str | None = Security(API_KEY_HEADER)) -> str:
    """
    Retrieves and validates the API key from the request headers.

    Raises:
        HTTPException: If the API key is missing, invalid, or not configured.
    """
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API Key is missing."
        )
    if api_key_header != CORTEX_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key."
        )
    return api_key_header
