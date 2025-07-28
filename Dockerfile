# Use a lightweight Python base image compatible with AMD64
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy your script and requirements
COPY extract_outline.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create input and output folders
RUN mkdir -p /app/input /app/output

# Set entrypoint to run your script automatically
CMD ["python", "extract_outline.py"]