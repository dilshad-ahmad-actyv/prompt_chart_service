import time
import logging
import concurrent.futures
from qdrant_client.models import VectorParams, Distance
import uuid
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ensure_collection_exists(client, collection_name, vector_size):
    """
    Ensure the collection exists. Create it if it doesn't.
    
    Args:
        client (QdrantClient): Qdrant client instance.
        collection_name (str): Name of the collection.
        vector_size (int): Size of the vectors.
    """
    try:
        # Check if the collection exists
        if collection_name not in [col.name for col in client.get_collections().collections]:
            logging.info(f"Collection '{collection_name}' does not exist. Creating it.")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
    except Exception as e:
        logging.error(f"Failed to ensure collection exists: {e}")
        raise

def retry_upsert(client, collection_name, points, retries=3, delay=5):
    logging.info('Vectors collection ------------->', points)
    
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

    # Ensure the collection exists
    ensure_collection_exists(client, collection_name, vector_size)
    
    # Prepare batches and upsert in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(valid_chunks), batch_size):
            batch_chunks = valid_chunks[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            unique_id = str(uuid.uuid4())
            points = [
                {
                    "id": unique_id,
                    "vector": embedding,
                    "payload": {"source": f"{unique_id}", "document": chunk},
                }
                for chunk, embedding in zip(batch_chunks, batch_embeddings)
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
