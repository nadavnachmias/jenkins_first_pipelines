#!/usr/bin/env python3
from server import app
import unittest
from datetime import datetime
import sys  # Required for sys.exit()


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        print("\n[DEBUG] Initializing test environment...")
        app.config['TESTING'] = True
        self.client = app.test_client()
        print("[DEBUG] Test client ready")

    def test_time_endpoint(self):
        print("\n[DEBUG] === Testing /time endpoint ===")
        
        print("[DEBUG] Making GET request to /time")
        response = self.client.get('/time')
        print(f"[DEBUG] Received status: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        print("[DEBUG] ✓ Status code 200 verified")
        
        response_text = response.get_data(as_text=True)
        print(f"[DEBUG] Full response: {response_text}")
        
        self.assertTrue("Current time is:" in response_text)
        print("[DEBUG] ✓ Found expected response text")
        
        time_str = response.get_data(as_text=True).split(": ")[1].strip()
        print(f"[DEBUG] Extracted time string: '{time_str}'")
        
        try:
            datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            print("[DEBUG] ✓ Time format validation passed")
        except ValueError as e:
            print(f"[DEBUG] ❌ Time format validation failed: {e}")
            self.fail("Time format is incorrect")

    def test_echo_endpoint(self):
        print("\n[DEBUG] === Testing /echo endpoint ===")
        test_message = "debug_test_123"
        print(f"[DEBUG] Using test message: '{test_message}'")
        
        print(f"[DEBUG] Making GET request to /echo/{test_message}")
        response = self.client.get(f'/echo/{test_message}')
        print(f"[DEBUG] Received status: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        print("[DEBUG] ✓ Status code 200 verified")
        
        actual_response = response.get_data(as_text=True)
        expected_response = f"You said: {test_message}"
        print(f"[DEBUG] Expected: '{expected_response}'")
        print(f"[DEBUG] Received: '{actual_response}'")
        
        self.assertEqual(actual_response, expected_response)
        print("[DEBUG] ✓ Response content matches exactly")

if __name__ == "__main__":
    print("[DEBUG] Starting test suite...")
    runner = unittest.TextTestRunner(verbosity=2)
    result = unittest.main(testRunner=runner, exit=False)
    if result.result.wasSuccessful():
        print("OK - All tests passed")  # This will be our success marker
        sys.exit(0)
    else:
        sys.exit(1)  # Non-zero for test failures
