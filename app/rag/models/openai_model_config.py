import openai
from dotenv import load_dotenv
import os
from openai import OpenAIError, AuthenticationError, RateLimitError

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise EnvironmentError("OPENAI_API_KEY is not set in the environment variables.")

def generate_openai_response(prompt, context, model):
    # Validate inputs
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string.")
    if not isinstance(context, str) or not context.strip():
        raise ValueError("Context must be a non-empty string.")
    
    # Prepare the messages for OpenAI Chat API
    messages = [
        {
            "role": "system",
            "content": (
                "You are a knowledgeable assistant. Use the provided context to answer questions accurately. "
                "All responses must be based only on the provided context. Do not infer or use external sources. "
                "If the information is not present in the Context, state that explicitly. "
                "If the question is not related to the document context but pertains to greetings, basic and formal conversations, you are allowed to respond appropriately. "
                "Always maintain 100% accuracy based on the context provided in step-by-step points where applicable."
            ),
        },
        {
            "role": "system",
            "content": f"Context:\n{context}",
        },
        {
            "role": "user",
            "content": (
                "Using the provided context, answer the following question with step-by-step accuracy:\n"
                f"{prompt}"
            ),
        },
    ]

    try:
        # Call OpenAI's ChatCompletion API
        response = openai.chat.completions.create(
            model=model, # "gpt-4",  # Use the desired GPT model
            messages=messages,
            # temperature=0.7,  # Balance creativity and accuracy
        )

        # Extract and return the assistant's reply
        return response.choices[0].message.content.strip()

    except AuthenticationError:
        raise Exception("Authentication failed. Please check your OpenAI API key.")
    except RateLimitError:
        raise Exception("Rate limit exceeded. Please wait and try again later.")
    except OpenAIError as e:
        raise Exception(f"OpenAI API error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")