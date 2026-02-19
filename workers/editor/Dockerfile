FROM python:3.11-slim

WORKDIR /app

# Install FFmpeg (non-GPU version for compatibility)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install supabase python-dotenv

COPY . .

CMD ["python", "worker.py"]
