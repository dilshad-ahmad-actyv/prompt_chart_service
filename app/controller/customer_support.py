# customer_support.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.rag.query_service import query_relevant_chunks
from app.services.openai_service import generate_openai_response

router = APIRouter()

@router.post("/chatbot")
async def chatbot(user_prompt: str, collection_name: str):
    """
    Handles the user prompt, queries the Qdrant vector database, and generates a response using OpenAI.

    Args:
        user_prompt (str): The prompt or query from the user.
        collection_name (str): The name of the Qdrant collection to query.

    Returns:
        JSONResponse: The generated response and relevant context.
    """
    try:
        # Query the relevant chunks from the database
        relevant_chunks = query_relevant_chunks(user_prompt, collection_name, top_k=5)

        # If no relevant chunks are found, return a response indicating that
        if not relevant_chunks:
            raise HTTPException(status_code=404, detail="No relevant chunks found in the collection.")

        # Generate OpenAI response based on the user prompt and relevant chunks
        response = generate_openai_response(user_prompt, relevant_chunks)

        # Return the response
        return JSONResponse(
            status_code=200,
            content={
                "response": response,
            },
        )
    except HTTPException as e:
        # Handle HTTP-specific exceptions
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})
    except Exception as e:
        # Handle unexpected errors
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred", "details": str(e)},
        )
