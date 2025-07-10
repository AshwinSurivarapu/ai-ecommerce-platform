# services/python/ai-chat-service/Dockerfile
FROM python:3.11-slim-buster

# Set the working dzirectory in the container to /app
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy config.yaml to the /app directory
COPY config.yaml ./

# Copy the entire 'python_service' directory into '/app/python_service'
# This creates the package structure inside the container.
COPY python_service/ ./python_service/

# Expose the port the Flask app runs on
EXPOSE 5000

# Define the command to run the Flask application
# FLASK_APP now points to the 'app' module inside the 'python_service' package.
ENV FLASK_APP=python_service.app
# Run the 'app' module from the 'python_service' package as the main script.
CMD ["python", "-m", "python_service.app"]