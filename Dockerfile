# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install packages directly (no requirements.txt needed)
RUN pip install --no-cache-dir flask requests

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=server.py

# Run server.py when the container launches
CMD ["python", "server.py"]
