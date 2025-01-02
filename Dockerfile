# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install dependencies for ODBC
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    libodbc1 \
    && rm -rf /var/lib/apt/lists/*
    
# Set the working directory in the container
WORKDIR /app

COPY requirements.txt ./
# Install dependencies
# Install the required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that Uvicorn will run on
EXPOSE 8000

# Command to run Uvicorn with FastAPI
# '--reload' is only for development; remove it for production
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
