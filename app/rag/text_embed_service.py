import os
import openai
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

openai_api_key = os.getenv("OPENAI_API_KEY")
embed_model = os.getenv("EMBEDDING_MODEL")

if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY is not set. Please provide it in the environment variables.")

openai.api_key = openai_api_key

# Initialize the OpenAI Embeddings model
try:
    embedding_model = OpenAIEmbeddings(model=embed_model)
except Exception as e:
    raise RuntimeError(f"Failed to initialize OpenAIEmbeddings: {e}")

def text_embed_service(chunks):
    """
    Embeds document chunks using OpenAI and returns a list of embeddings.

    Args:
        chunks (list): A list of text chunks to embed.

    Returns:
        list: A list of embeddings corresponding to the input chunks.

    Raises:
        ValueError: If `chunks` is not a list or is empty.
        RuntimeError: If embedding fails due to API or model issues.
    """
    # Validate input
    if not isinstance(chunks, list):
        raise ValueError("Input `chunks` must be a list of strings.")
    if len(chunks) == 0:
        logging.warning("The `chunks` list is empty. Returning an empty embeddings list.")
        return []
    if not all(isinstance(chunk, str) for chunk in chunks):
        raise ValueError("All items in `chunks` must be strings.")

    try:
        # Log the number of chunks being embedded
        logging.info(f"Embedding {len(chunks)} chunks using OpenAI model {embedding_model}.")
        embeddings = embedding_model.embed_documents(chunks)
        logging.info("Embedding completed successfully.")
        return embeddings
    except openai.error.AuthenticationError:
        logging.error("Authentication failed. Check your OpenAI API key.")
        raise RuntimeError("Authentication failed. Ensure your OpenAI API key is valid.")
    except openai.error.APIError as api_error:
        logging.error(f"API error occurred: {api_error}")
        raise RuntimeError(f"API error occurred: {api_error}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while embedding chunks: {e}")
        raise RuntimeError(f"An unexpected error occurred: {e}")


    # try:
    #     embeddings = embed_chunks(chunks)
    #     print(f"Generated {len(embeddings)} embeddings.")
    # except Exception as e:
    #     print(f"Error: {e}")