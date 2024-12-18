# openai_service.py

import openai
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_openai_response(prompt, relevant_chunks):
    """
    Uses OpenAI to generate a response based on the user prompt and relevant document chunks.

    Args:
        prompt (str): The user prompt.
        relevant_chunks (list): List of relevant document chunks to provide context.

    Returns:
        str: The generated response from OpenAI.
    """
    # Combine relevant chunks and prompt
    context = "\n".join([chunk["document"] for chunk in relevant_chunks])
    # complete_prompt = f"User Query: {prompt}\n\nContext:\n{context}\n\nGenerate a concise, accurate response based on the context."
    messages = [
            {"role": "system", "content": "You are a knowledgeable assistant. Use the provided context to answer questions accurately."},
            {"role": "system", "content": f"Context:\n{context}"},
            {"role": "user", "content": prompt},
        ]
    try:

        # Create messages for GPT-4 Chat API

        
                # Call OpenAI's ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=200,  # Adjust max tokens based on expected output length
            temperature=0.7,  # Balance creativity and accuracy
        )

        # Extract and return the assistant's reply
        return response["choices"][0]["message"]["content"]
    
        # Call OpenAI to generate the response
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=complete_prompt,
        #     # max_tokens=150,
        #     n=1,
        #     stop=None,
        #     temperature=0.7,
        # )

        # answer = response.choices[0].text.strip()
        # return answer
    except openai.error.OpenAIError as e:
        raise Exception(f"OpenAI API error: {e}")
