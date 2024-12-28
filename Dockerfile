# Use Python as base image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Start the Flask server
CMD ["python", "server.py"]
