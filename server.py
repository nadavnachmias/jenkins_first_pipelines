#!/usr/bin/env python3
from flask import Flask
from datetime import datetime

app = Flask(__name__)

# Endpoint 1: Get current time
@app.route('/time')
def get_time():
    # Get the current time in a human-readable format
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time is: {current_time}"

# Endpoint 2: Echo back the client's message
@app.route('/echo/<message>')
def echo(message):
    return f"You said: {message}"

@app.route('/about_git')
def about_git_page():
    return "this is a feature for my brand new git branch"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
