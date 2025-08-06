#!/usr/bin/env python3
"""
Simple test script for HackRx API endpoint
Uses a local file instead of downloading from URL
"""

import requests
import json
import time

# Configuration
API_BASE = "http://127.0.0.1:8000"
API_TOKEN = "8b796ad826037b97ba28ae4cd36c4605bd9ed1464673ad5b0a3290a9867a9d21"

# Simple test data with local file
test_payload = {
    "documents": "file://C:/COG/uploads/test_policy.txt",  # Use local file
    "questions": [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?"
    ]
}

def test_hackrx_run():
    """Test the /api/v1/hackrx/run endpoint."""
    print("🚀 Testing /api/v1/hackrx/run endpoint...")
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/api/v1/hackrx/run",
            headers=headers,
            json=test_payload,
            timeout=30  # Reduced timeout
        )
        end_time = time.time()
        
        print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ HackRx API call successful!")
            print(f"📝 Number of answers: {len(result.get('answers', []))}")
            
            for i, answer in enumerate(result.get('answers', [])):
                print(f"\n📋 Answer {i+1}:")
                print(f"   Question: {test_payload['questions'][i]}")
                print(f"   Answer: {answer[:200]}...")
                
        else:
            print(f"❌ HackRx API call failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (30 seconds)")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health():
    """Test the health endpoint."""
    print("🔍 Testing /api/v1/health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/v1/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

if __name__ == "__main__":
    print("🧪 Simple HackRx API Test")
    test_health()
    test_hackrx_run() 