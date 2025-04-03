#!/usr/bin/env python3
import unittest
import requests
import argparse
import os

# Set up argument parsing with environment variable fallback
parser = argparse.ArgumentParser()
default_url = f"http://localhost:{os.getenv('APP_PORT', '5000')}"  # Use APP_PORT or default to 5000
parser.add_argument('--url', default=default_url, help='Base URL of the Flask app')
args = parser.parse_args()

class TestFlaskEndpoints(unittest.TestCase):
    """Basic tests for the Flask server endpoints."""

    def test_time_endpoint(self):
        """Test if /time returns a valid timestamp."""
        response = requests.get(f"{args.url}/time")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Current time is:", response.text)
        print("✅ /time endpoint test passed")

    def test_echo_endpoint(self):
        """Test if /echo returns the correct message."""
        test_message = "hello_jenkins"
        response = requests.get(f"{args.url}/echo/{test_message}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"You said: {test_message}", response.text)
        print("✅ /echo endpoint test passed")

    def test_about_git_endpoint(self):
        """Test if /about_git returns the expected string."""
        response = requests.get(f"{args.url}/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn("this is server num 1 welcome !", response.text)
        print("✅ /about_git endpoint test passed")

if __name__ == "__main__":
    # Run tests and exit with status code (0=success, 1=failure)
    try:
        unittest.main(argv=[''], exit=False)
        print("\n🔥 All tests passed! Proceed to Jenkins automation stages.")
        exit(0)
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        exit(1)
