# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies first (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies first (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

EXPOSE $PORT

HEALTHCHECK --interval=30s --timeout=3s \
CMD curl -f http://localhost:$PORT/about || exit 1

CMD ["flask", "run", "--host=0.0.0.0", "--port=$PORT"]


