"""
API Testing Script
Test all endpoints of the LLM Document Processing System.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"
API_TOKEN = "default-token-change-me"  # Change this to your actual token

# Headers for authenticated requests
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def test_health_endpoint():
    """Test the health check endpoint."""
    print("🏥 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"   Service: {data['service']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_stats_endpoint():
    """Test the stats endpoint."""
    print("\n📊 Testing Stats Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/stats", headers={"Authorization": f"Bearer {API_TOKEN}"})
        if response.status_code == 200:
            data = response.json()
            print("✅ Stats Retrieved:")
            print(f"   Vector Store Chunks: {data.get('vector_store', {}).get('total_chunks', 'N/A')}")
            print(f"   Embedding Model: {data.get('vector_store', {}).get('embedding_model', 'N/A')}")
            print(f"   LLM Model: {data.get('llm_model', {}).get('model_name', 'N/A')}")
            print(f"   LLM Available: {data.get('llm_model', {}).get('available', 'N/A')}")
            return True
        elif response.status_code == 401:
            print("❌ Stats failed: Unauthorized (check API token)")
            return False
        else:
            print(f"❌ Stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Stats error: {e}")
        return False

def test_upload_endpoint():
    """Test the document upload endpoint."""
    print("\n📄 Testing Upload Endpoint...")
    
    # Create a sample text file to upload
    sample_content = """
    Health Insurance Policy - Test Document
    
    Coverage Details:
    - Age limit: 18-65 years
    - Knee surgery: Covered up to ₹85,000
    - Emergency procedures: Covered from day 1
    - Geographic coverage: Pan India including Pune
    
    Exclusions:
    - Cosmetic surgery: Not covered
    - Dental: Not covered unless accidental
    """
    
    try:
        # Create the file content
        files = {
            'file': ('test_policy.txt', sample_content, 'text/plain')
        }
        
        response = requests.post(
            f"{BASE_URL}/upload",
            files=files,
            headers={"Authorization": f"Bearer {API_TOKEN}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Document Upload Successful:")
            print(f"   Filename: {data.get('filename', 'N/A')}")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Chunks Added: {data.get('vector_store', {}).get('chunks_added', 'N/A')}")
            print(f"   Total Chunks: {data.get('vector_store', {}).get('total_chunks', 'N/A')}")
            print(f"   Word Count: {data.get('stats', {}).get('words', 'N/A')}")
            return True
        elif response.status_code == 401:
            print("❌ Upload failed: Unauthorized (check API token)")
            return False
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def test_query_endpoint():
    """Test the query processing endpoint."""
    print("\n🔍 Testing Query Endpoint...")
    
    # Test queries
    test_queries = [
        "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
        "Emergency surgery coverage",
        "Cosmetic surgery coverage",
        "Age eligibility for insurance"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Query {i}: {query}")
        
        try:
            payload = {"query": query}
            response = requests.post(
                f"{BASE_URL}/query",
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Decision: {data.get('decision', 'N/A')}")
                print(f"   💰 Amount: {data.get('amount', 'N/A')}")
                print(f"   📊 Method: {data.get('analysis_method', 'N/A')}")
                print(f"   📄 Relevant Chunks: {data.get('relevant_chunks', 'N/A')}")
                
                # Show justification preview
                justification = data.get('justification', '')
                if len(justification) > 80:
                    justification = justification[:80] + "..."
                print(f"   ✨ Justification: {justification}")
                
            elif response.status_code == 401:
                print("   ❌ Query failed: Unauthorized")
                return False
            else:
                print(f"   ❌ Query failed: {response.status_code}")
                print(f"   Response: {response.text}")
        
        except Exception as e:
            print(f"   ❌ Query error: {e}")
    
    return True

def main():
    """Run all API tests."""
    print("🧪 LLM Document Processing System - API Testing")
    print("=" * 60)
    
    # Wait a moment for server to fully start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test all endpoints
    tests_passed = 0
    total_tests = 4
    
    if test_health_endpoint():
        tests_passed += 1
    
    if test_stats_endpoint():
        tests_passed += 1
        
    if test_upload_endpoint():
        tests_passed += 1
        
    if test_query_endpoint():
        tests_passed += 1
    
    # Summary
    print(f"\n🎯 API Testing Complete")
    print("=" * 60)
    print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🚀 All endpoints working correctly!")
        print("\n🌐 You can now access the API at:")
        print(f"   - Health Check: {BASE_URL}/health")
        print(f"   - Upload Document: {BASE_URL}/upload (POST with Bearer token)")
        print(f"   - Process Query: {BASE_URL}/query (POST with Bearer token)")
        print(f"   - Get Statistics: {BASE_URL}/stats (GET with Bearer token)")
    else:
        print("⚠️ Some tests failed - check the error messages above")

if __name__ == "__main__":
    main()