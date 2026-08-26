FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Environment variable for port with fallback
ENV PORT=8000

# Run FastAPI via uvicorn (Cloud Run dynamically sets $PORT)
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
