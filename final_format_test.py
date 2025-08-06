#!/usr/bin/env python3
"""
Final Format Test - Verifies exact response format matches problem statement
"""

import requests
import json

# Configuration
API_BASE = "http://127.0.0.1:8000"
API_TOKEN = "8b796ad826037b97ba28ae4cd36c4605bd9ed1464673ad5b0a3290a9867a9d21"

def test_exact_response_format():
    """Test that response format exactly matches problem statement specification."""
    
    print("🔍 FINAL RESPONSE FORMAT TEST")
    print("=" * 50)
    
    # Test with the exact payload from problem statement
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
        print("Testing exact response format...")
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
            result = response.json()
            
            print("✅ Response received successfully")
            print(f"   - Status code: {response.status_code}")
            print(f"   - Response type: {type(result)}")
            print(f"   - Response keys: {list(result.keys())}")
            
            # Check exact format requirements
            if 'answers' in result:
                print("✅ 'answers' key present")
                answers = result['answers']
                
                if isinstance(answers, list):
                    print("✅ 'answers' is a list")
                    print(f"   - Number of answers: {len(answers)}")
                    print(f"   - Expected answers: {len(test_payload['questions'])}")
                    
                    if len(answers) == len(test_payload['questions']):
                        print("✅ Number of answers matches number of questions")
                        
                        # Check each answer format
                        all_valid = True
                        for i, answer in enumerate(answers):
                            if isinstance(answer, str) and len(answer) > 0:
                                print(f"   ✅ Answer {i+1}: Valid string ({len(answer)} chars)")
                            else:
                                print(f"   ❌ Answer {i+1}: Invalid format")
                                all_valid = False
                        
                        if all_valid:
                            print("✅ All answers are valid strings")
                            
                            # Show sample answers
                            print("\n📋 SAMPLE ANSWERS:")
                            for i, answer in enumerate(answers[:3]):  # Show first 3
                                print(f"   Answer {i+1}: {answer[:100]}...")
                            
                            print("\n🎯 RESPONSE FORMAT VERIFICATION:")
                            print("✅ Matches problem statement specification exactly!")
                            print("✅ Ready for HackRx competition submission!")
                            
                        else:
                            print("❌ Some answers are not valid strings")
                    else:
                        print(f"❌ Answer count mismatch: {len(answers)} vs {len(test_payload['questions'])}")
                else:
                    print("❌ 'answers' is not a list")
            else:
                print("❌ 'answers' key missing")
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_exact_response_format() 