import os
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import ScoredPoint, VectorParams, Distance
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

def query_relevant_chunks(query, collection_name, top_k=5, embedding_model=None):
    """
    Queries the Qdrant database for the most relevant document chunks.

    Args:
        query (str): The search query.
        collection_name (str): The name of the Qdrant collection to query.
        top_k (int): The number of most relevant chunks to return. Default is 5.
        embedding_model (Callable): A function or model to generate embeddings for the query.

    Returns:
        list: A list of the top_k most relevant document chunks with their scores.
    """
    # Validate inputs
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string.")
    if not isinstance(collection_name, str) or not collection_name.strip():
        raise ValueError("Collection name must be a non-empty string.")
    if not embedding_model:
        raise ValueError("An embedding model must be provided to generate query embeddings.")

    try:
        # Generate query embedding
        logging.info(f"Generating embedding for the query: '{query}'")
        query_embedding = embedding_model.embed_query(query)

        # Check if the collection exists
        if not client.get_collections().has_collection(collection_name):
            raise ValueError(f"Collection '{collection_name}' does not exist in Qdrant.")

        # Perform the search in Qdrant
        logging.info(f"Searching for the top {top_k} relevant chunks in collection '{collection_name}'.")
        search_results = client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=top_k,
        )

        # Parse results
        results = [
            {
                "id": point.id,
                "score": point.score,
                "document": point.payload.get("document", "No document available"),
                "source": point.payload.get("source", "Unknown source")
            }
            for point in search_results
        ]

        logging.info(f"Found {len(results)} relevant chunks.")
        return results

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred during query: {e}")
        raise RuntimeError(f"Query failed due to an unexpected error: {e}")


# if __name__ == "__main__":
#     # Example usage
#     from langchain_community.embeddings import OpenAIEmbeddings

#     # Initialize the embedding model
#     embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

#     # Define the query and collection name
#     query = "What is natural language processing?"
#     collection_name = "my_collection"

#     try:
#         results = query_relevant_chunks(query, collection_name, top_k=5, embedding_model=embedding_model)
#         for idx, result in enumerate(results, start=1):
#             print(f"Result {idx}:")
#             print(f"  Document: {result['document']}")
#             print(f"  Source: {result['source']}")
#             print(f"  Score: {result['score']:.4f}")
#     except Exception as e:
#         logging.error(f"Error while querying: {e}")
