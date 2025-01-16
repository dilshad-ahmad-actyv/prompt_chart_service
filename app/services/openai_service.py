import openai
import logging
from dotenv import load_dotenv
import os
from openai import OpenAIError, AuthenticationError, RateLimitError
from rag.models.openai_model_config import generate_openai_response
from rag.models.deepseek_model_config import generate_deepseek_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("application.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    logging.critical("OPENAI_API_KEY is not set in the environment variables.")
    raise EnvironmentError("OPENAI_API_KEY is required but not found in environment variables.")

def generate_response(prompt, relevant_chunks, model):
    """
    Generate a response using OpenAI or DeepSeek models based on the user prompt and relevant document chunks.

    Args:
        prompt (str): The user prompt.
        relevant_chunks (list): List of relevant document chunks to provide context.
        model (str): The model to use ('openai' or 'deepseek').

    Returns:
        str: The generated response from the selected model.
    """
    if not prompt or not isinstance(prompt, str):
        logging.error("Invalid prompt: Prompt must be a non-empty string.")
        raise ValueError("Prompt must be a non-empty string.")

    if not relevant_chunks or not isinstance(relevant_chunks, list):
        logging.error("Invalid relevant_chunks: Must be a non-empty list of documents.")
        raise ValueError("Relevant chunks must be a non-empty list of documents.")

    # Combine relevant chunks to form the context
    context = "\n".join(chunk.get("document", "No content available") for chunk in relevant_chunks)

    try:
        if model in ['gpt-4', 'gpt-3.5-turbo']:
            logging.info(f"Generating response using OpenAI model: {model}.")
            response = generate_openai_response(prompt, context, model)
        elif model == 'deepseek-chat':
            logging.info("Generating response using DeepSeek model.")
            response = generate_deepseek_response(prompt, context, model)
        else:
            logging.error("Invalid model specified: Must be 'gpt-4', 'gpt-3.5-turbo', or 'deepseek'.")
            raise ValueError("Invalid model. Choose 'gpt-4', 'gpt-3.5-turbo', or 'deepseek'.")

        return response
    except AuthenticationError:
        logging.error("Authentication failed. Check your API key.")
        raise
    except RateLimitError:
        logging.warning("Rate limit exceeded. Please try again later.")
        return "Rate limit exceeded. Please wait and try again."
    except OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return f"An error occurred while using the OpenAI API: {e}"
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        raise
