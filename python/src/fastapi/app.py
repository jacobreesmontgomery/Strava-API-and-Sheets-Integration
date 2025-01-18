"""
CLASS: app.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will drive the front-end webpage.
"""

# IMPORTS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.activities_api import router as activities_router
import os
from dotenv import load_dotenv

from utilities.simple_logger import SimpleLogger

logger = SimpleLogger(log_level="INFO", class_name=__name__).logger

# Load environment variables
load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
AUTH_EXCHANGE_LINK = os.environ.get("AUTH_EXCHANGE_LINK")

app = FastAPI()

app.include_router(
    router=activities_router,
    prefix="/api/v1",
    tags=["Activities"],
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=5000)
