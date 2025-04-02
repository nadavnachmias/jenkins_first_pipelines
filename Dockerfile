FROM python:3.12-slim

WORKDIR /app

COPY . /app

# Install packages directly (no requirements.txt needed)
RUN pip install --no-cache-dir flask requests
RUN pip install pytest  # Install pytest as well

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=server.py

# Run server.py when the container launches
CMD ["python", "server.py"]
