# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run application
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
