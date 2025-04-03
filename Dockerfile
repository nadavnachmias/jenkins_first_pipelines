FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV FLASK_APP=server.py
ENV FLASK_ENV=production  # Or 'development' if needed

# Document the port (optional but recommended)
EXPOSE 5000

# Run the app (ensure it listens on 0.0.0.0 for Docker)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
