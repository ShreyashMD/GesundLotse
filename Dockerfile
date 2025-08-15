FROM python:3.11-slim

WORKDIR /app

# Keep Python lean + set writable Hugging Face cache paths
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/.cache/huggingface \
    HUGGINGFACE_HUB_CACHE=/app/.cache/huggingface \
    TRANSFORMERS_CACHE=/app/.cache/huggingface/transformers \
    SENTENCE_TRANSFORMERS_HOME=/app/.cache/sentence-transformers

# Create cache dirs and make them writable
RUN mkdir -p /app/.cache/huggingface /app/.cache/sentence-transformers && chmod -R 777 /app/.cache

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 7860

# Run the Flask app
CMD ["python", "app.py"]
