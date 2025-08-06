#!/usr/bin/env python3
"""
Quick test to identify issues with the HackRx API.
"""

import requests
import json

# Configuration
API_BASE = "http://127.0.0.1:8000"
API_TOKEN = "8b796ad826037b97ba28ae4cd36c4605bd9ed1464673ad5b0a3290a9867a9d21"

def test_basic_functionality():
    """Test basic API functionality."""
    
    print("🔍 QUICK SYSTEM TEST")
    print("=" * 40)
    
    # Test 1: Health endpoint
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/v1/health")
        if response.status_code == 200:
            print("✅ Health endpoint: WORKING")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint: FAILED - {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint: ERROR - {e}")
    
    # Test 2: Simple query
    print("\n2️⃣ Testing simple query...")
    try:
        test_payload = {
            "documents": "file://C:/COG/uploads/test_policy.txt",
            "questions": ["What is the grace period?"]
        }
        
        response = requests.post(
            f"{API_BASE}/api/v1/hackrx/run",
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {API_TOKEN}'
            },
            json=test_payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Simple query: WORKING")
            result = response.json()
            print(f"   Answers: {len(result.get('answers', []))}")
        else:
            print(f"❌ Simple query: FAILED - {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Simple query: ERROR - {e}")

if __name__ == "__main__":
    test_basic_functionality() 