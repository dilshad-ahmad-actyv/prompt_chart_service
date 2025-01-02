from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import logging
from app.rag.file_reader import FileReader
from app.rag.file_upload import upload_file 

router = APIRouter()


@router.post("/upload")
async def upload_and_read_file(file: UploadFile = File(...)):
    """
    API endpoint to upload a file and read its content.

    Args:
        file (UploadFile): The file to upload.

    Returns:
        JSONResponse: Metadata about the uploaded file and its content.
    """
    try:
        print(file)

        # Save the file using the utility function
        file_path = upload_file(file)
    
        # Read the file content using FileReader
        file_reader = FileReader()
        content = []
        for chunk in file_reader.read_file(file_path):
            print('single chunk: ', chunk)
            content.append(chunk)

        # Return file details and content
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded and read successfully.",
                "file_name": file.filename,
                "file_path": file_path,
                "content": content[:5],  # Return the first 5 chunks/pages for demonstration
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
