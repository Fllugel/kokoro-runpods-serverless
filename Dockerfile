# Use the existing working Kokoro FastAPI image as base
FROM ghcr.io/remsky/kokoro-fastapi-gpu:latest

# Reset entrypoint to avoid conflicts with base image
ENTRYPOINT []

# Copy the serverless handler
COPY handler.py /app/handler.py

# Switch to root to install runpod in the existing virtual environment
USER root

# Install system dependencies and runpod in a single layer for better caching
RUN echo "--- Environment Check ---" && \
    ls -la /app && \
    which python && \
    python --version && \
    echo "-------------------------" && \
    apt-get update && \
    apt-get install -y git curl && \
    rm -rf /var/lib/apt/lists/* && \
    python -m ensurepip --upgrade || (curl -sS https://bootstrap.pypa.io/get-pip.py | python) && \
    python -m pip install --no-cache-dir runpod>=1.0.0 --break-system-packages || python -m pip install --no-cache-dir runpod>=1.0.0

# Switch back to appuser
USER appuser

# Set environment variables for the wrapper
ENV PYTHONPATH=/app:/app/api

# Point HuggingFace cache to network volume (persistent storage)
ENV HF_HOME=/runpod-volume
ENV TRANSFORMERS_CACHE=/runpod-volume
ENV HF_HUB_CACHE=/runpod-volume

# Run the serverless handler directly with unbuffered output
CMD ["python", "-u", "/app/handler.py"]
