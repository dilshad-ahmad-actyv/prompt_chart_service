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

if not QDRANT_URL or not QDRANT_API_KEY:
    raise EnvironmentError("QDRANT_URL or QDRANT_API_KEY is not set in the environment variables.")

# Configure Qdrant client
try:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
except Exception as e:
    raise RuntimeError(f"Failed to connect to Qdrant: {e}")


def retry_upsert(client, collection_name, points, retries=3, delay=5):
    """
    Retry logic for upserting data into Qdrant.

    Args:
        client (QdrantClient): Qdrant client instance.
        collection_name (str): Name of the Qdrant collection.
        points (list): Points to upsert.
        retries (int): Number of retry attempts.
        delay (int): Delay in seconds between retries.

    Raises:
        Exception: If all retries fail.
    """
    for attempt in range(retries):
        try:
            client.upsert(collection_name=collection_name, points=points)
            logging.info(f"Batch successfully upserted.")
            return
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt + 1 < retries:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("Max retries reached. Operation failed.")
                raise


def parallel_upsert(client, collection_name, chunks, embeddings, batch_size=50):
    """
    Handles parallel upserts for chunks and embeddings to Qdrant.

    Args:
        client (QdrantClient): Qdrant client instance.
        collection_name (str): Name of the Qdrant collection.
        chunks (list): List of text chunks.
        embeddings (list): List of corresponding embeddings.
        batch_size (int): Number of points per batch.

    Returns:
        None
    """
    # Validate inputs
    if not isinstance(chunks, list) or not isinstance(embeddings, list):
        raise ValueError("Both `chunks` and `embeddings` must be lists.")
    if len(chunks) == 0 or len(embeddings) == 0:
        logging.warning("Chunks or embeddings are empty. Nothing to upsert.")
        return
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings must have the same length.")

    # Validate each chunk and embedding
    valid_chunks = [chunk for chunk in chunks if isinstance(chunk, str) and chunk.strip()]
    if not valid_chunks:
        logging.error("No valid chunks found. Exiting...")
        return

    vector_size = len(embeddings[0])  # Determine vector size from the first embedding
    if not all(len(embedding) == vector_size for embedding in embeddings):
        raise ValueError("All embeddings must have the same vector size.")

    try:
        # Recreate the collection
        logging.info(f"Recreating collection '{collection_name}' with vector size {vector_size}.")
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
    except Exception as e:
        logging.error(f"Failed to recreate collection: {e}")
        raise

    # Prepare batches and upsert in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(valid_chunks), batch_size):
            batch_chunks = valid_chunks[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            points = [
                {
                    "id": i + j,
                    "vector": embedding,
                    "payload": {"source": f"chunk_{i + j}", "document": chunk},
                }
                for j, (chunk, embedding) in enumerate(zip(batch_chunks, batch_embeddings))
            ]

            # Submit upsert task for each batch
            futures.append(executor.submit(retry_upsert, client, collection_name, points))

        # Wait for all futures to complete and check for exceptions
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Raises exception if the task failed
            except Exception as e:
                logging.error(f"Error during parallel upsert: {e}")
                raise

    logging.info("All batches have been upserted successfully.")


# if __name__ == "__main__":
#     # Example usage
#     chunks = ["This is a test chunk.", "Another example chunk."]
#     embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]  # Example embeddings

#     try:
#         parallel_upsert(client, "test_collection", chunks, embeddings, batch_size=1)
#     except Exception as e:
#         logging.error(f"Critical error: {e}")
