from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import logging
from app.rag.file_reader import FileReader
from app.rag.file_upload import upload_file
from app.rag.text_chunk_service import split_text_into_chunks
from app.rag.text_embed_service import text_embed_service
from app.rag.vector_store import parallel_upsert
from app.rag.model_configs import client

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@router.post("/upload/file")
async def upload_and_read_file(
    file: UploadFile = File(...),
     collection_name: str = Query(..., description="Name of the collection to store embeddings")
     ):
    """
    API endpoint to upload a file and read its content.

    Args:
        file (UploadFile): The file to upload.

    Returns:
        JSONResponse: Metadata about the uploaded file and its content.
    """
    try:
        logging.info(f"Received file: {file.filename}")

        # Save the file using the utility function
        file_path = upload_file(file)
        logging.info(f"File saved to: {file_path}")
        
        # Read the file content using FileReader
        file_reader = FileReader()
        
        content = ''
        for chunk in file_reader.read_file(file_path):
            print('single chunk-->: ', chunk)
            # content.append(chunk)
            content += " " + chunk
        
        logging.info("File content successfully read.")
        
        # split the content into chunks
        chunks = split_text_into_chunks(content)
        logging.info(f"Split content into {len(chunks)} chunks.")
        
        # convert the chunks into embeddings
        embeddings = text_embed_service(chunks)
        logging.info(f"Generated embeddings for {len(chunks)} chunks.")
         
        # store the chunks and embedding into the vector database
        parallel_upsert(client, collection_name, chunks, embeddings, batch_size=50)
        logging.info(f"Data successfully upserted into collection: {collection_name}")
         
       # Return success response
        return JSONResponse(
            status_code=200,
            content={
                "message": "File processed and data stored successfully.",
                "file_name": file.filename,
                "collection_name": collection_name,
                "chunk_count": len(chunks),
            },
        )
    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during file upload and reading."
        )
