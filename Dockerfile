# Use a base Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies in a virtual environment
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=server.py
ENV FLASK_ENV=production

# Expose the port that the app will run on
EXPOSE 5000

# Set the entrypoint to activate the virtual environment and run the Flask app
CMD ["/app/venv/bin/python", "server.py"]
