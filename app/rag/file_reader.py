import os
import time
import logging
from PyPDF2 import PdfReader

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class FileReader:
    """
    A utility class for reading files of types '.txt' and '.pdf' in a streaming way.
    Handles retries and resumes reading from the last read position in case of errors.
    """

    def __init__(self, chunk_size=1024, max_retries=3, retry_delay=2):
        """
        Initializes the FileReader.

        Args:
            chunk_size (int): The size of each chunk to read from the file. Defaults to 1024 bytes.
            max_retries (int): The maximum number of retries in case of errors. Defaults to 3.
            retry_delay (int): The delay (in seconds) between retries. Defaults to 2 seconds.
        """
        self.chunk_size = chunk_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def read_txt_file(self, file_path):
        """
        Reads a '.txt' file in a streaming way.

        Args:
            file_path (str): The path to the '.txt' file.

        Yields:
            str: A chunk of the file content.
        """
        logging.info(f"Reading TXT file: {file_path}")
        position = 0  # Track the current position in the file

        for attempt in range(self.max_retries):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file.seek(position)  # Resume from the last position
                    while chunk := file.read(self.chunk_size):
                        position += len(chunk)
                        yield chunk
                return  # Exit after successful reading
            except Exception as e:
                logging.error(f"Error reading TXT file (Attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt + 1 < self.max_retries:
                    logging.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logging.critical("Max retries reached. Could not complete reading the file.")
                    raise

    def read_pdf_file(self, file_path):
        """
        Reads a '.pdf' file in a streaming way.

        Args:
            file_path (str): The path to the '.pdf' file.

        Yields:
            str: A page of the PDF content.
        """
        logging.info(f"Reading PDF file: {file_path}")
        position = 0  # Track the current page

        for attempt in range(self.max_retries):
            try:
                pdf_reader = PdfReader(file_path)
                total_pages = len(pdf_reader.pages)
                for page_number in range(position, total_pages):
                    try:
                        text = pdf_reader.pages[page_number].extract_text()
                        position = page_number + 1
                        if text:
                            yield text
                    except Exception as e:
                        logging.warning(f"Error reading page {page_number + 1}: {e}")
                        continue  # Skip problematic pages
                return  # Exit after successful reading
            except Exception as e:
                logging.error(f"Error reading PDF file (Attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt + 1 < self.max_retries:
                    logging.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logging.critical("Max retries reached. Could not complete reading the PDF file.")
                    raise

    def read_file(self, file_path):
        """
        Reads a file based on its type ('.txt' or '.pdf').

        Args:
            file_path (str): The path to the file.

        Yields:
            str: A chunk or page of the file content.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_extension = os.path.splitext(file_path)[-1].lower()
        if file_extension == ".txt":
            yield from self.read_txt_file(file_path)
        elif file_extension == ".pdf":
            yield from self.read_pdf_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")


# Example Usage
# if __name__ == "__main__":
#     file_reader = FileReader(chunk_size=1024)

#     # Example file paths
#     txt_file_path = "example.txt"
#     pdf_file_path = "example.pdf"

#     # Reading a TXT file
#     try:
#         for chunk in file_reader.read_file(txt_file_path):
#             print(chunk)  # Process the chunk (e.g., store or analyze)
#     except Exception as e:
#         logging.error(f"Failed to read TXT file: {e}")

#     # Reading a PDF file
#     try:
#         for page in file_reader.read_file(pdf_file_path):
#             print(page)  # Process the page (e.g., store or analyze)
#     except Exception as e:
#         logging.error(f"Failed to read PDF file: {e}")




# Returning as a whole file
#----------------------------------------------------------------------------------

# class FileReader:
#     ...
#     def read_txt_file(self, file_path):
#         """
#         Reads a '.txt' file and returns the entire content as a single string.

#         Args:
#             file_path (str): The path to the '.txt' file.

#         Returns:
#             str: The full content of the '.txt' file.
#         """
#         logging.info(f"Reading TXT file: {file_path}")
#         content = ""
#         for attempt in range(self.max_retries):
#             try:
#                 with open(file_path, "r", encoding="utf-8") as file:
#                     while chunk := file.read(self.chunk_size):
#                         content += chunk  # Append the chunk to the content
#                 return content  # Return the full content after reading all chunks
#             except Exception as e:
#                 logging.error(f"Error reading TXT file (Attempt {attempt + 1}/{self.max_retries}): {e}")
#                 if attempt + 1 < self.max_retries:
#                     logging.info(f"Retrying in {self.retry_delay} seconds...")
#                     time.sleep(self.retry_delay)
#                 else:
#                     logging.critical("Max retries reached. Could not complete reading the file.")
#                     raise

#     def read_pdf_file(self, file_path):
#         """
#         Reads a '.pdf' file and returns the entire content as a single string.

#         Args:
#             file_path (str): The path to the '.pdf' file.

#         Returns:
#             str: The full content of the '.pdf' file.
#         """
#         logging.info(f"Reading PDF file: {file_path}")
#         content = ""
#         for attempt in range(self.max_retries):
#             try:
#                 pdf_reader = PdfReader(file_path)
#                 total_pages = len(pdf_reader.pages)
#                 for page_number in range(total_pages):
#                     try:
#                         text = pdf_reader.pages[page_number].extract_text()
#                         if text:
#                             content += text  # Append the text of the page to the content
#                     except Exception as e:
#                         logging.warning(f"Error reading page {page_number + 1}: {e}")
#                         continue  # Skip problematic pages
#                 return content  # Return the full content after reading all pages
#             except Exception as e:
#                 logging.error(f"Error reading PDF file (Attempt {attempt + 1}/{self.max_retries}): {e}")
#                 if attempt + 1 < self.max_retries:
#                     logging.info(f"Retrying in {self.retry_delay} seconds...")
#                     time.sleep(self.retry_delay)
#                 else:
#                     logging.critical("Max retries reached. Could not complete reading the PDF file.")
#                     raise

# # Reading a TXT file
# try:
#     content = file_reader.read_file(txt_file_path)  # This will return the entire content
#     print(content)  # Process the content
# except Exception as e:
#     logging.error(f"Failed to read TXT file: {e}")

# # Reading a PDF file
# try:
#     content = file_reader.read_file(pdf_file_path)  # This will return the entire content
#     print(content)  # Process the content
# except Exception as e:
#     logging.error(f"Failed to read PDF file: {e}")
