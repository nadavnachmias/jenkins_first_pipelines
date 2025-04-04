# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_ENV=production

# Expose port (documentation only)
EXPOSE 5000

# Health check (using container's internal port 5000)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/about || exit 1

# Run command (fixed internal port)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
