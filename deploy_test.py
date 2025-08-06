#!/usr/bin/env python3
"""
Deployment Test Script - Tests the deployed API
"""

import requests
import json
import time

# Configuration - Replace with your deployed URL
DEPLOYED_URL = "https://your-app-name.onrender.com"  # Replace with your actual URL
API_TOKEN = "8b796ad826037b97ba28ae4cd36c4605bd9ed1464673ad5b0a3290a9867a9d21"

def test_deployed_api():
    """Test the deployed API endpoints."""
    
    print("🔍 DEPLOYMENT TEST")
    print("=" * 50)
    print(f"Testing deployed API: {DEPLOYED_URL}")
    print()
    
    # Test 1: Health endpoint
    print("1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{DEPLOYED_URL}/api/v1/health", timeout=30)
        if response.status_code == 200:
            print("✅ Health endpoint: WORKING")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint: FAILED - {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint: ERROR - {e}")
    
    # Test 2: Main API endpoint
    print("\n2️⃣ Testing main API endpoint...")
    test_payload = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?"
        ]
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{DEPLOYED_URL}/api/v1/hackrx/run",
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {API_TOKEN}'
            },
            json=test_payload,
            timeout=60
        )
        end_time = time.time()
        
        if response.status_code == 200:
            print("✅ Main API endpoint: WORKING")
            result = response.json()
            print(f"   - Response time: {end_time - start_time:.2f}s")
            print(f"   - Answers received: {len(result.get('answers', []))}")
            print(f"   - Expected answers: {len(test_payload['questions'])}")
            
            if len(result.get('answers', [])) == len(test_payload['questions']):
                print("✅ Answer count: CORRECT")
            else:
                print("❌ Answer count: MISMATCH")
                
        else:
            print(f"❌ Main API endpoint: FAILED - {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Main API endpoint: ERROR - {e}")
    
    # Test 3: Authentication
    print("\n3️⃣ Testing authentication...")
    try:
        response = requests.post(
            f"{DEPLOYED_URL}/api/v1/hackrx/run",
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            json=test_payload,
            timeout=30
        )
        
        if response.status_code == 401:
            print("✅ Authentication: WORKING")
        else:
            print(f"❌ Authentication: FAILED - {response.status_code}")
            
    except Exception as e:
        print(f"❌ Authentication test: ERROR - {e}")
    
    # Test 4: HTTPS
    print("\n4️⃣ Testing HTTPS...")
    if DEPLOYED_URL.startswith('https://'):
        print("✅ HTTPS: ENABLED")
    else:
        print("❌ HTTPS: NOT ENABLED")
    
    print("\n" + "=" * 50)
    print("🎯 DEPLOYMENT TEST COMPLETED")
    print("=" * 50)
    
    print("\n📋 NEXT STEPS:")
    print("1. If all tests pass, your API is ready for submission!")
    print("2. Submit your webhook URL to HackRx:")
    print(f"   {DEPLOYED_URL}/api/v1/hackrx/run")
    print("3. Add description: 'Flask + FAISS + Sentence Transformers + LLM'")

if __name__ == "__main__":
    test_deployed_api() 