#! /usr/bin/python3
"""Main function for running the API service."""
# mypy: ignore-errors
import uvicorn
from app import create_application
from app.configs import get_settings

app = create_application()
settings = get_settings()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5500, reload=True)  # nosec
