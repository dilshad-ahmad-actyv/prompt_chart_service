import os
from pathlib import Path

# Directory for uploaded files
UPLOAD_DIR = Path("../uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure directory exists


def upload_file(file) -> str:
    """
    Handles file upload by saving it to the uploads directory.

    Args:
        file (UploadFile): The file to be uploaded.

    Returns:
        str: The path to the saved file.

    Raises:
        ValueError: If the file type is unsupported.
    """
    # Validate file type
    allowed_extensions = {"txt", "pdf"}
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        raise ValueError(f"Unsupported file type: {file_extension}. Allowed types: {', '.join(allowed_extensions)}")

    # Save the file
    file_path = UPLOAD_DIR / file.filename
    print('Saving file', file_path)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return str(file_path)
