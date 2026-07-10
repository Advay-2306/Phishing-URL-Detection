# Base image - Official Python 3.12 slim version (lightweight, good for production)
FROM python:3.12-slim

# Set the working directory inside the container
# All subsequent commands will run from this folder
WORKDIR /app

# Copy requirements.txt first (this layer is cached if requirements don't change)
# This makes rebuilding the image much faster
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir : keeps image size small by not storing pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
# This includes your Python code, folders, etc.
COPY . .

# Create necessary directories (e.g., for models, database files, etc.)
# -p flag prevents error if directory already exists
RUN mkdir -p models

# Tell Docker that the container listens on port 8000
EXPOSE 8000

# Command that runs when the container starts
# Here it's starting the FastAPI app using Uvicorn
# ml_service.main:app means:
#   - Look for 'main.py' inside 'ml_service' folder
#   - Run the 'app' object (FastAPI instance)
CMD ["uvicorn", "ml_service.main:app", "--host", "0.0.0.0", "--port", "8000"]