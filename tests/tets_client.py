#!/usr/bin/env python3
import pytest
from server import app
from datetime import datetime
import sys

@pytest.fixture
def client():
    """Pytest fixture providing a test client"""
    print("\n[DEBUG] Initializing test client...")
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    print("[DEBUG] Test client closed")

def test_time_endpoint(client):
    """Test /time endpoint with debug messages"""
    print("\n[DEBUG] === Testing /time endpoint ===")
    
    print("[DEBUG] Making GET request to /time")
    response = client.get('/time')
    print(f"[DEBUG] Received status: {response.status_code}")
    
    assert response.status_code == 200
    print("[DEBUG] ✓ Status code 200 verified")
    
    response_text = response.get_data(as_text=True)
    print(f"[DEBUG] Full response: {response_text}")
    
    assert "Current time is:" in response_text
    print("[DEBUG] ✓ Found expected response text")
    
    time_str = response_text.split(": ")[1].strip()
    print(f"[DEBUG] Extracted time string: '{time_str}'")
    
    try:
        datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        print("[DEBUG] ✓ Time format validation passed")
    except ValueError as e:
        print(f"[DEBUG] ❌ Time format validation failed: {e}")
        pytest.fail("Time format is incorrect")

def test_echo_endpoint(client):
    """Test /echo endpoint with debug messages"""
    print("\n[DEBUG] === Testing /echo endpoint ===")
    test_message = "pytest_debug_123"
    print(f"[DEBUG] Using test message: '{test_message}'")
    
    print(f"[DEBUG] Making GET request to /echo/{test_message}")
    response = client.get(f'/echo/{test_message}')
    print(f"[DEBUG] Received status: {response.status_code}")
    
    assert response.status_code == 200
    print("[DEBUG] ✓ Status code 200 verified")
    
    actual_response = response.get_data(as_text=True)
    expected_response = f"You said: {test_message}"
    print(f"[DEBUG] Expected: '{expected_response}'")
    print(f"[DEBUG] Received: '{actual_response}'")
    
    assert actual_response == expected_response
    print("[DEBUG] ✓ Response content matches exactly")

if __name__ == "__main__":
    print("[DEBUG] Starting pytest test suite...")
    
    # Run pytest with:
    # - Verbose output (-v)
    # - JUnit XML reporting (for Jenkins)
    # - Disable pytest's exit so we can print our OK message
    exit_code = pytest.main(["-v", "--junitxml=test-results.xml"])
    
    # Print final OK message if all tests passed (exit code 0)
    if exit_code == 0:
        print("\nOK - All tests passed")
    
    # Explicitly exit with pytest's status code
    sys.exit(exit_code)
