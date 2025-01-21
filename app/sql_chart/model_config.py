import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from openai import OpenAI, OpenAIError, AuthenticationError, RateLimitError
from dotenv import load_dotenv
import os
# from config.settings import DEEPSEEK_BASE_URL, DEEPSEEK_API_KEY

DEEPSEEK_API_KEY='sk-adb871a1db8a4d2a969b91772056aec1'
DEEPSEEK_BASE_URL='https://api.deepseek.com'

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

if not DEEPSEEK_API_KEY:
    logging.error("DEEPSEEK_API_KEY is not set in environment variables.")
    raise EnvironmentError("DEEPSEEK_API_KEY is required but not found in environment variables.")

if not DEEPSEEK_BASE_URL:
    logging.error("DEEPSEEK_BASE_URL is not set in environment variables.")
    raise EnvironmentError("DEEPSEEK_BASE_URL is required but not found in environment variables.")

# Initialize the OpenAI client for DeepSeek
try:
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
except Exception as e:
    logging.critical(f"Failed to initialize OpenAI client: {e}")
    raise

def generate_response(prompt, system_prompt):
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
        response = client.chat.completions.create(
            model= "deepseek-chat",
            messages=messages,
            stream=False
        )

        if not response.choices or not response.choices[0].message.content:
            logging.warning("Response received, but no content was found.")
            return "No response generated. Please try again."

        res = response.choices[0].message.content.strip()
        # print('Response received: ', res)
        return res

    except AuthenticationError:
        logging.error("Authentication failed. Check your DeepSeek API key.")
        raise
    except RateLimitError:
        logging.warning("Rate limit exceeded. Retrying after a delay.")
        # You could implement a retry mechanism here if needed.
        return "Rate limit exceeded. Please wait and try again."
    except OpenAIError as e:
        logging.error(f"DeepSeek API error: {e}")
        return f"An error occurred: {e}"
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        raise
