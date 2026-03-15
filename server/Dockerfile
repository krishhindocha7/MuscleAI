#Dockerfile (backend)
FROM python:3.11-slim

# -- Basics --
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

# -- Install system dependencies --
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# -- Install Python dependencies --
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# -- Copy application code --
COPY . /app/

# -- Expose the port the app runs on --
EXPOSE 8000

# -- Run the application --
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]