FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PyMuPDF and FAISS
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run the backend using the module flag as we practiced
CMD ["python", "-m", "api.main"]