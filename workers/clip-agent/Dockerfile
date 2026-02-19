FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg yt-dlp \
    && rm -rf /var/lib/apt/lists/*

RUN pip install supabase python-dotenv

COPY . .

CMD ["python", "worker.py"]
