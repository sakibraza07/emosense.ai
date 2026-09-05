# Hugging Face Spaces (Docker SDK) deployment for EmoSense AI

FROM python:3.11-slim

# ffmpeg is required by pydub to convert uploaded webm audio to wav
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render assigns its own port at runtime via $PORT -- default to 10000
# locally/for other platforms that don't set it.
ENV PORT=10000
EXPOSE 10000

# Shell form (not exec array form) so $PORT actually gets expanded at runtime.
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 \
    --worker-class sync --timeout 120 --max-requests 100

