import sys
import os
import time
import logging
import concurrent.futures
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Validate environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# if not QDRANT_URL or not QDRANT_API_KEY:
if not QDRANT_URL:
    raise EnvironmentError("QDRANT_URL or QDRANT_API_KEY is not set in the environment variables.")

# Configure Qdrant client
try:
    # client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    client = QdrantClient(url=QDRANT_URL)
except Exception as e:
    raise RuntimeError(f"Failed to connect to Qdrant: {e}")