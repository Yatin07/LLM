#!/usr/bin/env python3
"""
Problem Statement Test - Verifies system against exact HackRx requirements
"""

import requests
import json
import time

# Configuration
API_BASE = "http://127.0.0.1:8000"
API_TOKEN = "8b796ad826037b97ba28ae4cd36c4605bd9ed1464673ad5b0a3290a9867a9d21"

def test_problem_statement_requirements():
    """Test all requirements from the problem statement."""
    
    print("🔍 PROBLEM STATEMENT REQUIREMENTS TEST")
    print("=" * 60)
    
    # Test 1: Required API Structure
    print("\n1️⃣ REQUIRED API STRUCTURE")
    print("-" * 40)
    
    # Test POST /hackrx/run endpoint
    test_payload = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?",
            "What is the No Claim Discount (NCD) offered in this policy?",
            "Is there a benefit for preventive health check-ups?",
            "How does the policy define a 'Hospital'?",
            "What is the extent of coverage for AYUSH treatments?",
            "Are there any sub-limits on room rent and ICU charges for Plan A?"
        ]
    }
    
    try:
        print("Testing POST /api/v1/hackrx/run endpoint...")
        response = requests.post(
            f"{API_BASE}/api/v1/hackrx/run",
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {API_TOKEN}'
            },
            json=test_payload,
            timeout=60
        )
        
        if response.status_code == 200:
            print("✅ POST /hackrx/run endpoint: WORKING")
            result = response.json()
            print(f"   - Response format: {type(result)}")
            print(f"   - Answers array: {len(result.get('answers', []))} items")
            print(f"   - Response time: {response.elapsed.total_seconds():.2f}s")
            
            # Check if response matches expected format
            if 'answers' in result and isinstance(result['answers'], list):
                print("✅ Response format: CORRECT")
                for i, answer in enumerate(result['answers'][:3]):  # Show first 3 answers
                    print(f"   - Answer {i+1}: {answer[:100]}...")
            else:
                print("❌ Response format: INCORRECT")
        else:
            print(f"❌ POST /hackrx/run endpoint: FAILED - {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ POST /hackrx/run endpoint: ERROR - {e}")
    
    # Test 2: Authentication
    print("\n2️⃣ AUTHENTICATION")
    print("-" * 40)
    
    try:
        # Test without authentication
        response = requests.post(
            f"{API_BASE}/api/v1/hackrx/run",
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            json=test_payload,
            timeout=30
        )
        
        if response.status_code == 401:
            print("✅ Authentication required: WORKING")
        else:
            print(f"❌ Authentication required: FAILED - {response.status_code}")
            
    except Exception as e:
        print(f"❌ Authentication test: ERROR - {e}")
    
    # Test 3: Request Format Validation
    print("\n3️⃣ REQUEST FORMAT VALIDATION")
    print("-" * 40)
    
    try:
        # Test missing documents field
        invalid_payload = {
            "questions": ["What is the grace period?"]
        }
        
        response = requests.post(
            f"{API_BASE}/api/v1/hackrx/run",
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {API_TOKEN}'
            },
            json=invalid_payload,
            timeout=30
        )
        
        if response.status_code == 400:
            print("✅ Missing documents validation: WORKING")
        else:
            print(f"❌ Missing documents validation: FAILED - {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request validation test: ERROR - {e}")
    
    # Test 4: Response Format
    print("\n4️⃣ RESPONSE FORMAT")
    print("-" * 40)
    
    try:
        # Test with simple payload
        simple_payload = {
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
            json=simple_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'answers' in result and isinstance(result['answers'], list):
                print("✅ Response format: CORRECT")
                print(f"   - Structure: {list(result.keys())}")
                print(f"   - Answers type: {type(result['answers'])}")
                print(f"   - Number of answers: {len(result['answers'])}")
            else:
                print("❌ Response format: INCORRECT")
        else:
            print(f"❌ Response format test: FAILED - {response.status_code}")
            
    except Exception as e:
        print(f"❌ Response format test: ERROR - {e}")
    
    # Test 5: Performance Requirements
    print("\n5️⃣ PERFORMANCE REQUIREMENTS")
    print("-" * 40)
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/api/v1/hackrx/run",
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {API_TOKEN}'
            },
            json=simple_payload,
            timeout=30
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response_time < 30:
            print(f"✅ Response time: {response_time:.2f}s (under 30s limit)")
        else:
            print(f"❌ Response time: {response_time:.2f}s (over 30s limit)")
            
    except Exception as e:
        print(f"❌ Performance test: ERROR - {e}")
    
    # Test 6: Error Handling
    print("\n6️⃣ ERROR HANDLING")
    print("-" * 40)
    
    try:
        # Test invalid JSON
        response = requests.post(
            f"{API_BASE}/api/v1/hackrx/run",
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {API_TOKEN}'
            },
            data="invalid json",
            timeout=30
        )
        
        if response.status_code == 400:
            print("✅ Invalid JSON handling: WORKING")
        else:
            print(f"❌ Invalid JSON handling: FAILED - {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error handling test: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print("🎯 PROBLEM STATEMENT TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_problem_statement_requirements() 