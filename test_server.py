#!/usr/bin/env python3
"""
Simple test script to verify the student server is working.
"""

import requests
import json

def test_server():
    base_url = "http://localhost:8000"
    
    # Test the mock evaluation endpoint
    print("Testing mock evaluation endpoint...")
    try:
        response = requests.post(
            f"{base_url}/eval-mock",
            json={"test": "data", "status": "ok"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing eval-mock: {e}")
    
    # Test the main API endpoint with a sample request
    print("\nTesting main API endpoint...")
    try:
        sample_request = {
            "email": "test@example.com",
            "secret": "test-secret-123",
            "task": "test-task",
            "round": 1,
            "nonce": "test-nonce",
            "brief": "Test brief for a simple web page",
            "checks": [],
            "evaluation_url": "http://localhost:8000/eval-mock",
            "attachments": []
        }
        
        response = requests.post(
            f"{base_url}/api-endpoint",
            json=sample_request
        )
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing api-endpoint: {e}")

if __name__ == "__main__":
    test_server()
