import requests
import json
from datetime import datetime

class UniversalPlatformTester:
    def __init__(self, base_url="https://portal-rescue.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🌐 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:300]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

def main():
    print("🚀 UNIVERSAL CUSTOMER INTELLIGENCE PLATFORM - FOCUSED TESTING")
    print("=" * 80)
    
    tester = UniversalPlatformTester()
    
    # Test Universal Platform endpoints
    print("\n1. Testing Universal Connectors Status...")
    success, response = tester.run_test(
        "Universal Connectors Status",
        "GET",
        "api/universal/connectors/status",
        200,
        timeout=30
    )
    
    print("\n2. Testing Universal Add Connector...")
    stripe_connector_data = {
        "platform_type": "stripe",
        "credentials": {
            "api_key": "sk_test_mock_key_for_testing",
            "webhook_secret": "whsec_mock_webhook_secret"
        }
    }
    success, response = tester.run_test(
        "Add Stripe Connector (Mock)",
        "POST",
        "api/universal/connectors/add",
        200,
        data=stripe_connector_data,
        timeout=30
    )
    
    print("\n3. Testing Universal Customers...")
    success, response = tester.run_test(
        "Universal Unified Customers",
        "GET",
        "api/universal/customers",
        200,
        timeout=45
    )
    
    print("\n4. Testing Universal Intelligence...")
    success, response = tester.run_test(
        "Universal Business Intelligence",
        "GET",
        "api/universal/intelligence",
        200,
        timeout=60
    )
    
    print("\n5. Testing Universal Dashboard...")
    success, response = tester.run_test(
        "Universal Dashboard",
        "GET",
        "api/universal/dashboard",
        200,
        timeout=45
    )
    
    print("\n6. Testing Universal Recommendations...")
    success, response = tester.run_test(
        "Universal Action Recommendations",
        "GET",
        "api/universal/recommendations",
        200,
        timeout=45
    )
    
    print("\n7. Testing Universal Sync...")
    success, response = tester.run_test(
        "Universal Platform Sync",
        "POST",
        "api/universal/sync",
        200,
        timeout=60
    )
    
    # Print results
    print(f"\n{'='*80}")
    print(f"📊 UNIVERSAL PLATFORM TEST RESULTS")
    print(f"{'='*80}")
    print(f"Tests run: {tester.tests_run}")
    print(f"Tests passed: {tester.tests_passed}")
    print(f"Success rate: {(tester.tests_passed/tester.tests_run*100):.1f}%" if tester.tests_run > 0 else "No tests run")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    main()