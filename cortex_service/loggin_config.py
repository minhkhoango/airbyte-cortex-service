# Pylance strict mode
import logging
import sys
from pythonjsonlogger import json

def configure_logging() -> None:
    """Configures structured JSON logging for the application."""
    log = logging.getLogger()
    log.setLevel(logging.WARNING)

    # Prevent duplicate logs if already configured
    if log.hasHandlers():
        log.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)

    # These are example fields. You can add more context as needed.
    supported_fields = [
        "asctime",
        "levelname",
        "message",
        "pathname",
        "funcName",
        "lineno",
    ]

    log_format = " ".join([f"%({field})s" for field in supported_fields])
    formatter = json.JsonFormatter(log_format)

    handler.setFormatter(formatter)
    log.addHandler(handler)