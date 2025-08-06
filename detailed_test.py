#!/usr/bin/env python3
"""
Detailed test to identify issues with the HackRx API.
"""

import requests
import json

# Configuration
API_BASE = "http://127.0.0.1:8000"
API_TOKEN = "8b796ad826037b97ba28ae4cd36c4605bd9ed1464673ad5b0a3290a9867a9d21"

def test_detailed_functionality():
    """Test detailed API functionality."""
    
    print("🔍 DETAILED SYSTEM TEST")
    print("=" * 50)
    
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
    
    # Test 2: Simple query with detailed error checking
    print("\n2️⃣ Testing simple query with error checking...")
    try:
        test_payload = {
            "documents": "file://C:/COG/uploads/test_policy.txt",
            "questions": ["What is the grace period?"]
        }
        
        print(f"   Sending payload: {json.dumps(test_payload, indent=2)}")
        
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
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Simple query: WORKING")
            result = response.json()
            print(f"   Answers: {len(result.get('answers', []))}")
            print(f"   First answer: {result.get('answers', [''])[0][:100]}...")
        else:
            print(f"❌ Simple query: FAILED - {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Simple query: ERROR - {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Multiple questions
    print("\n3️⃣ Testing multiple questions...")
    try:
        test_payload = {
            "documents": "file://C:/COG/uploads/test_policy.txt",
            "questions": [
                "What is the grace period for premium payment?",
                "What is the waiting period for pre-existing diseases?"
            ]
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
        
        if response.status_code == 200:
            print("✅ Multiple questions: WORKING")
            result = response.json()
            print(f"   Answers: {len(result.get('answers', []))}")
            for i, answer in enumerate(result.get('answers', [])):
                print(f"   Answer {i+1}: {answer[:100]}...")
        else:
            print(f"❌ Multiple questions: FAILED - {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Multiple questions: ERROR - {e}")
    
    # Test 4: Natural language query
    print("\n4️⃣ Testing natural language query...")
    try:
        test_payload = {
            "documents": "file://C:/COG/uploads/test_policy.txt",
            "questions": [
                "Does this policy cover knee surgery, and what are the conditions?"
            ]
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
        
        if response.status_code == 200:
            print("✅ Natural language query: WORKING")
            result = response.json()
            print(f"   Answer: {result.get('answers', [''])[0][:200]}...")
        else:
            print(f"❌ Natural language query: FAILED - {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Natural language query: ERROR - {e}")

if __name__ == "__main__":
    test_detailed_functionality() 