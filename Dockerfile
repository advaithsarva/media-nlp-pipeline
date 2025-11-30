FROM python:3.10-slim

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml requirements-dev.txt ./

# Install pip dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy project files
COPY . .

# Expose API port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "src.api.service:app", "--host", "0.0.0.0", "--port", "8000"]
