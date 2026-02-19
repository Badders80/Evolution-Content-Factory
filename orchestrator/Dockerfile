# FastAPI backend - API documentation coming in Phase 2
# For now, this is a placeholder that will be replaced with full implementation
# once Supabase credentials are provided

FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn supabase python-dotenv

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
