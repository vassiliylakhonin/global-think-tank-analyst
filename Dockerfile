FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (required for some C-extensions like FAISS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy repository files
COPY . .

# Install the Python package with all necessary extras for the full toolkit
RUN pip install --no-cache-dir -e ".[ui,enterprise,agent]"

# Expose ports for FastAPI (8000) and Streamlit UI (8501)
EXPOSE 8000 8501

# Default to running the API server
CMD ["gtta", "server", "--host", "0.0.0.0", "--port", "8000"]
