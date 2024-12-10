# # main.py
import sys
import os
# import glob
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from scripts.pdf_reader import read_pdf
# from scripts.chunker import split_large_chunk
# from scripts.embedder import embed_chunks
# from scripts.qdrant_store import store_in_qdrant

# def main(folder_path):
#     # Use glob to find all PDF files in the specified folder
#     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    
#     for file_path in pdf_files:
#         print(f"Processing file: {file_path}")
        
#         # Step 1: Read PDF
#         text = read_pdf(file_path)
#         if not text:
#             print(f"Failed to read document: {file_path}")
#             continue
        
#         # Step 2: Chunk the text
#         large_chunks = [split_large_chunk(text) for chunk in text]
#         # chunks = chunk_text(text, chunk_size=500)
        
#         # Step 3: Embed chunks
#         chunk_embeddings = embed_chunks(large_chunks)
        
#         # Step 4: Store in Qdrant
#         store_in_qdrant(large_chunks, chunk_embeddings)

# # Run the pipeline on all PDF files in the data/raw folder
# if __name__ == "__main__":
#     main("data/raw")



from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from scripts.qdrant_store import parallel_upsert, retry_upsert
from scripts.embedder import embed_chunks
from scripts.pdf_reader import read_pdf
from scripts.chunker import split_large_chunk
from qdrant_client import QdrantClient
from qdrant_client.models import Filter
import logging
import tempfile

logger = logging.getLogger("uvicorn.error")


# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure Qdrant client
client = QdrantClient(
    url=os.getenv("QDRANT_CLOUD_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collection_name = "documents"

class Chunk(BaseModel):
    id: int
    vector: List[float]
    payload: dict


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@app.get('/hello')
def hello() :
     return {"message": "Hello World!"}

@app.post("/upload")
async def upsert_data(file: UploadFile = File(...)):
    """
    Endpoint to upsert data into Qdrant
    """
    try:
        if not file:
            return {"message": "No upload file sent"}
            
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        text = read_pdf(temp_file_path)

        if not text:
            raise ValueError("File is empty or unreadable.")
        
        chunks = split_large_chunk(text)

        if not chunks:
            raise ValueError("No valid chunks extracted from the document.")
        
        embeddings = embed_chunks(chunks)

        if not embeddings:
            raise ValueError("Failed to generate embeddings for the chunks.")
        
        parallel_upsert(client, collection_name, chunks, embeddings)
        return {"message": "Data uploaded successfully"}
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except TimeoutError as te:
        logger.error(f"Timeout error during upsert: {te}")
        raise HTTPException(status_code=504, detail="Timeout error. Please try again later.")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Error upserting data")


@app.post("/get")
async def get_data(query_request: QueryRequest):
    """
    Endpoint to retrieve data from Qdrant based on a query string
    """
    try:
        # Embed the query using the same model as used for chunks
        query_embedding = embed_chunks([query_request.query])
        
        # Perform similarity search in Qdrant
        results = client.search(
            collection_name="documents",
            query_vector=query_embedding[0],
            limit=query_request.top_k
        )
        
        if not results:
            return {"message": "No results found"}
        
        # Return top K results
        return {"results": [result.payload["document"] for result in results]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")


# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

