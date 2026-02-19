FROM python:3.11-slim

WORKDIR /app

RUN pip install supabase python-dotenv requests

COPY . .

CMD ["python", "worker.py"]
