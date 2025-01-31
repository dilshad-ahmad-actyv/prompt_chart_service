import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from openai import OpenAI, OpenAIError, AuthenticationError, RateLimitError
from dotenv import load_dotenv
import requests
# from config.settings import DEEPSEEK_BASE_URL, DEEPSEEK_API_KEY

DEEPSEEK_API_KEY= os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL= os.getenv("DEEPSEEK_BASE_URL")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("application.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

# Load environment variables
load_dotenv()

if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY is not set in environment variables.")
    raise EnvironmentError("OPENAI_API_KEY is required but not found in environment variables.")
    
if not DEEPSEEK_API_KEY:
    logging.error("DEEPSEEK_API_KEY is not set in environment variables.")
    raise EnvironmentError("DEEPSEEK_API_KEY is required but not found in environment variables.")

if not DEEPSEEK_BASE_URL:
    logging.error("DEEPSEEK_BASE_URL is not set in environment variables.")
    raise EnvironmentError("DEEPSEEK_BASE_URL is required but not found in environment variables.")

def generate_response(prompt, system_prompt, model="deepseek-chat"):
    """
    Generate a response using the specified model type.

    :param prompt: User input as a string.
    :param system_prompt: System prompt to guide the conversation.
    :param model_type: The model to use ("openai" or "deepseek"). Default is "openai".
    :return: Generated response as a string.
    """
    if not prompt or not isinstance(prompt, str):
        logging.error("Invalid prompt: Prompt must be a non-empty string.")
        raise ValueError("Prompt must be a non-empty string.")

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt
        },
    ]

    try:
        if model in ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"]:
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=model,  # Use OpenAI's model
                messages=messages,
                stream=False,
                temperature=0
            )
        elif model in ["deepseek-chat", "deepseek-reasoner"]:
            try:
                client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
            except Exception as e:
                logging.critical(f"Failed to initialize OpenAI client: {e}")
                raise
            response = client.chat.completions.create(
                model=model,  # Use DeepSeek's model
                messages=messages,
                stream=False,
                temperature=0
            )
        else:
            logging.error(f"Invalid model type: {model}")
            raise ValueError("Invalid model type. Supported types are 'openai' and 'deepseek'.")

        logging.debug(f"Raw API response: {response}")

        if not response.choices or not response.choices[0].message.content:
            logging.warning("Response received, but no content was found.")
            return "No response generated. Please try again."

        res = response.choices[0].message.content.strip()
        return res

    except AuthenticationError:
        logging.error(f"Authentication failed. Check your {model} API key.")
        raise
    except RateLimitError:
        logging.warning("Rate limit exceeded. Retrying after a delay.")
        return "Rate limit exceeded. Please wait and try again."
    except OpenAIError as e:
        logging.error(f"{model} API error: {e}")
        return f"An error occurred: {e}"
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        raise