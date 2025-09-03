# Pylance strict mode
import os
from dotenv import load_dotenv
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional

# Load environment variables from .env file
load_dotenv()

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
CORTEX_API_KEY: Optional[str] = os.getenv("CORTEX_API_KEY")

def get_api_key(api_key_header: Optional[str] = Security(API_KEY_HEADER)) -> str:
    """
    Retrieves and validates the API key from the request headers.
    
    Raises:
        HTTPException: If the API key is missing, invalid, or not configured.
    """
    if CORTEX_API_KEY is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API Key not configured on the server."
        )
    if api_key_header is None:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is missing."
        )
    if api_key_header != CORTEX_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key."
        )
    return api_key_header