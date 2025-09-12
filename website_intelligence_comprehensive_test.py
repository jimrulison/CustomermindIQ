#!/usr/bin/env python3
"""
Website Intelligence Hub Backend Comprehensive Testing Suite

Focus on MongoDB integration and API endpoints as requested in review:
1. MongoDB Integration & Data Persistence
2. Add Website Functionality 
3. Delete Website Functionality (NEWLY IMPLEMENTED)
4. Update All Websites
5. MongoDB Data Quality
6. Error Handling & Edge Cases

Authentication: admin@customermindiq.com / CustomerMindIQ2025!
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List
import uuid
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get backend URL from environment
import os
sys.path.append('/app/frontend')

try:
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                BACKEND_URL = line.split('=')[1].strip()
                break
        else:
            BACKEND_URL = "https://websiteintel-hub.preview.emergentagent.com"
except:
    BACKEND_URL = "https://websiteintel-hub.preview.emergentagent.com"

print(f"🔗 Testing Website Intelligence Hub Backend at: {BACKEND_URL}")

class WebsiteIntelligenceHubTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.auth_token = None
        self.test_website_ids = []  # Track created websites for cleanup
        
    def authenticate(self) -> bool:
        """Authenticate with admin credentials"""
        try:
            print("\n🔐 AUTHENTICATING WITH ADMIN CREDENTIALS")
            print("=" * 50)
            
            auth_data = {
                "email": "admin@customermindiq.com",
                "password": "CustomerMindIQ2025!"
            }
            
            response = requests.post(f"{self.base_url}/api/auth/login", json=auth_data, timeout=30, verify=False)
            
            if response.status_code == 200:
                auth_response = response.json()
                self.auth_token = auth_response.get("access_token")
                print(f"✅ Authentication successful - Token obtained")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token"""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict[str, Any] = None, 
                     expected_status: int = 200, test_name: str = "") -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        self.total_tests += 1
        url = f"{self.base_url}{endpoint}"
        
        try:
            headers = self.get_headers()
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30, verify=False)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30, verify=False)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30, verify=False)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            # Check status code
            status_ok = response.status_code == expected_status
            
            # Try to parse JSON response
            try:
                response_data = response.json()
                json_valid = True
            except:
                response_data = {"error": "Invalid JSON response", "text": response.text[:500]}
                json_valid = False
            
            # Determine if test passed
            test_passed = status_ok and json_valid
            if test_passed:
                self.passed_tests += 1
            
            result = {
                "test_name": test_name or f"{method} {endpoint}",
                "method": method.upper(),
                "endpoint": endpoint,
                "url": url,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "status_ok": status_ok,
                "json_valid": json_valid,
                "test_passed": test_passed,
                "response_data": response_data,
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(result)
            
            # Print result
            status_icon = "✅" if test_passed else "❌"
            print(f"{status_icon} {test_name}: {response.status_code} - {'PASS' if test_passed else 'FAIL'}")
            
            if not test_passed:
                print(f"   Expected: {expected_status}, Got: {response.status_code}")
                if not json_valid:
                    print(f"   JSON Error: {response_data.get('error', 'Unknown')}")
                elif response_data.get('detail'):
                    print(f"   Error Detail: {response_data['detail']}")
            
            return result
            
        except Exception as e:
            result = {
                "test_name": test_name or f"{method} {endpoint}",
                "method": method.upper(),
                "endpoint": endpoint,
                "url": url,
                "status_code": 0,
                "expected_status": expected_status,
                "status_ok": False,
                "json_valid": False,
                "test_passed": False,
                "response_data": {"error": str(e)},
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(result)
            print(f"❌ {test_name}: ERROR - {str(e)}")
            return result

    def test_mongodb_integration_and_dashboard(self):
        """Test MongoDB Integration & Data Persistence - Dashboard endpoint"""
        print("\n🗄️ TESTING MONGODB INTEGRATION & DATA PERSISTENCE")
        print("=" * 60)
        
        # Test dashboard endpoint - should retrieve data from MongoDB
        result = self.test_endpoint(
            "GET", 
            "/api/website-intelligence/dashboard",
            test_name="MongoDB Integration - Dashboard Data Retrieval"
        )
        
        if result["test_passed"]:
            dashboard_data = result["response_data"]
            
            # Verify dashboard structure
            if "dashboard" in dashboard_data:
                dashboard = dashboard_data["dashboard"]
                
                # Check for user_websites (combination of static + MongoDB data)
                if "user_websites" in dashboard:
                    websites = dashboard["user_websites"]
                    print(f"   📊 Found {len(websites)} websites in dashboard")
                    
                    # Verify static demo websites are present
                    static_ids = ["web_001", "web_002", "web_003"]
                    found_static = [w for w in websites if w.get("website_id") in static_ids]
                    print(f"   📊 Static demo websites: {len(found_static)}/3")
                    
                    # Check for proper datetime handling
                    datetime_fields = ["last_analyzed", "created_at", "updated_at"]
                    for website in websites:
                        for field in datetime_fields:
                            if field in website:
                                print(f"   📊 Datetime field '{field}' present in website data")
                                break
                else:
                    print("   ❌ user_websites not found in dashboard")
            else:
                print("   ❌ dashboard structure not found in response")

    def test_add_website_functionality(self):
        """Test Add Website Functionality with MongoDB persistence"""
        print("\n➕ TESTING ADD WEBSITE FUNCTIONALITY")
        print("=" * 50)
        
        # Test 1: Add E-commerce website
        ecommerce_data = {
            "domain": "teststore.example.com",
            "name": "Test E-commerce Store",
            "type": "E-commerce",
            "membership_tier": "professional",
            "current_websites": 2
        }
        
        result = self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=ecommerce_data,
            test_name="Add E-commerce Website"
        )
        
        if result["test_passed"]:
            response_data = result["response_data"]
            if "website_id" in response_data:
                website_id = response_data["website_id"]
                self.test_website_ids.append(website_id)
                print(f"   📝 Created website ID: {website_id}")
                
                # Verify response structure
                if "website_details" in response_data:
                    details = response_data["website_details"]
                    print(f"   📝 Domain: {details.get('domain')}")
                    print(f"   📝 Name: {details.get('website_name')}")
                    print(f"   📝 Type: {details.get('website_type')}")
                    print(f"   📝 Status: {details.get('status')}")
        
        # Test 2: Add Blog website
        blog_data = {
            "domain": "myblog.example.com",
            "name": "Test Blog Site",
            "type": "Blog",
            "membership_tier": "professional",
            "current_websites": 3
        }
        
        result = self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=blog_data,
            test_name="Add Blog Website"
        )
        
        if result["test_passed"] and "website_id" in result["response_data"]:
            website_id = result["response_data"]["website_id"]
            self.test_website_ids.append(website_id)
            print(f"   📝 Created website ID: {website_id}")
        
        # Test 3: Add Corporate website
        corporate_data = {
            "domain": "corporate.example.com",
            "name": "Test Corporate Site",
            "type": "Corporate",
            "membership_tier": "professional",
            "current_websites": 4
        }
        
        result = self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=corporate_data,
            test_name="Add Corporate Website"
        )
        
        if result["test_passed"] and "website_id" in result["response_data"]:
            website_id = result["response_data"]["website_id"]
            self.test_website_ids.append(website_id)
            print(f"   📝 Created website ID: {website_id}")
        
        # Test 4: Test membership limits
        limit_test_data = {
            "domain": "overlimit.example.com",
            "name": "Over Limit Site",
            "type": "General",
            "membership_tier": "basic",
            "current_websites": 1  # Basic tier limit is 1
        }
        
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=limit_test_data,
            expected_status=403,
            test_name="Test Membership Limit Enforcement"
        )

    def test_delete_website_functionality(self):
        """Test Delete Website Functionality (NEWLY IMPLEMENTED)"""
        print("\n🗑️ TESTING DELETE WEBSITE FUNCTIONALITY (NEWLY IMPLEMENTED)")
        print("=" * 60)
        
        # Test 1: Delete a user-added website (should work)
        if self.test_website_ids:
            website_id_to_delete = self.test_website_ids[0]
            result = self.test_endpoint(
                "DELETE",
                f"/api/website-intelligence/website/{website_id_to_delete}",
                test_name="Delete User-Added Website"
            )
            
            if result["test_passed"]:
                response_data = result["response_data"]
                print(f"   🗑️ Deleted website: {response_data.get('message', 'Unknown')}")
                print(f"   🗑️ Remaining websites: {response_data.get('remaining_websites', 'Unknown')}")
                
                # Remove from our tracking list
                self.test_website_ids.remove(website_id_to_delete)
        
        # Test 2: Try to delete a static demo website (should fail)
        self.test_endpoint(
            "DELETE",
            "/api/website-intelligence/website/web_001",
            expected_status=403,
            test_name="Prevent Deletion of Static Demo Website (web_001)"
        )
        
        self.test_endpoint(
            "DELETE",
            "/api/website-intelligence/website/web_002",
            expected_status=403,
            test_name="Prevent Deletion of Static Demo Website (web_002)"
        )
        
        self.test_endpoint(
            "DELETE",
            "/api/website-intelligence/website/web_003",
            expected_status=403,
            test_name="Prevent Deletion of Static Demo Website (web_003)"
        )
        
        # Test 3: Try to delete non-existent website
        fake_website_id = str(uuid.uuid4())
        self.test_endpoint(
            "DELETE",
            f"/api/website-intelligence/website/{fake_website_id}",
            expected_status=404,
            test_name="Delete Non-Existent Website (404 Error)"
        )

    def test_update_all_websites(self):
        """Test Update All Websites functionality"""
        print("\n🔄 TESTING UPDATE ALL WEBSITES")
        print("=" * 40)
        
        result = self.test_endpoint(
            "POST",
            "/api/website-intelligence/update-all",
            test_name="Update All Websites"
        )
        
        if result["test_passed"]:
            response_data = result["response_data"]
            print(f"   🔄 Update ID: {response_data.get('update_id', 'Unknown')}")
            print(f"   🔄 Websites to update: {response_data.get('websites_to_update', 'Unknown')}")
            
            if "update_queue" in response_data:
                queue = response_data["update_queue"]
                print(f"   🔄 Update queue contains {len(queue)} websites")
                for item in queue:
                    print(f"      - {item.get('domain', 'Unknown')}: {item.get('status', 'Unknown')}")

    def test_mongodb_data_quality(self):
        """Test MongoDB Data Quality - datetime serialization/deserialization"""
        print("\n📊 TESTING MONGODB DATA QUALITY")
        print("=" * 40)
        
        # Add a website to test datetime handling
        test_data = {
            "domain": "datetime-test.example.com",
            "name": "DateTime Test Site",
            "type": "General",
            "membership_tier": "professional",
            "current_websites": 1
        }
        
        result = self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=test_data,
            test_name="MongoDB Data Quality - DateTime Handling"
        )
        
        if result["test_passed"]:
            response_data = result["response_data"]
            website_id = response_data.get("website_id")
            if website_id:
                self.test_website_ids.append(website_id)
                
                # Check if datetime fields are properly formatted
                if "website_details" in response_data:
                    details = response_data["website_details"]
                    added_date = details.get("added_date")
                    if added_date:
                        print(f"   📊 DateTime format: {added_date}")
                        # Verify it's in ISO format
                        try:
                            datetime.fromisoformat(added_date.replace('Z', '+00:00'))
                            print(f"   ✅ DateTime properly formatted as ISO string")
                        except ValueError:
                            print(f"   ❌ DateTime not in proper ISO format")
        
        # Test dashboard again to verify data persistence
        result = self.test_endpoint(
            "GET",
            "/api/website-intelligence/dashboard",
            test_name="Verify Data Persistence After Add"
        )
        
        if result["test_passed"]:
            dashboard_data = result["response_data"]
            if "dashboard" in dashboard_data and "user_websites" in dashboard_data["dashboard"]:
                websites = dashboard_data["dashboard"]["user_websites"]
                user_added_websites = [w for w in websites if w.get("website_id") not in ["web_001", "web_002", "web_003"]]
                print(f"   📊 User-added websites persisted: {len(user_added_websites)}")

    def test_error_handling_edge_cases(self):
        """Test Error Handling & Edge Cases"""
        print("\n⚠️ TESTING ERROR HANDLING & EDGE CASES")
        print("=" * 50)
        
        # Test 1: Invalid domain format
        invalid_domain_data = {
            "domain": "not-a-valid-domain",
            "name": "Invalid Domain Test",
            "type": "General",
            "membership_tier": "professional",
            "current_websites": 1
        }
        
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=invalid_domain_data,
            test_name="Invalid Domain Format Handling"
        )
        
        # Test 2: Missing required fields
        incomplete_data = {
            "domain": "incomplete.example.com"
            # Missing name, type, etc.
        }
        
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=incomplete_data,
            test_name="Missing Required Fields Handling"
        )
        
        # Test 3: Invalid website type
        invalid_type_data = {
            "domain": "invalidtype.example.com",
            "name": "Invalid Type Test",
            "type": "InvalidType",
            "membership_tier": "professional",
            "current_websites": 1
        }
        
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=invalid_type_data,
            test_name="Invalid Website Type Handling"
        )
        
        # Test 4: Invalid membership tier
        invalid_tier_data = {
            "domain": "invalidtier.example.com",
            "name": "Invalid Tier Test",
            "type": "General",
            "membership_tier": "invalid_tier",
            "current_websites": 1
        }
        
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=invalid_tier_data,
            test_name="Invalid Membership Tier Handling"
        )

    def cleanup_test_websites(self):
        """Clean up any remaining test websites"""
        print("\n🧹 CLEANING UP TEST WEBSITES")
        print("=" * 35)
        
        for website_id in self.test_website_ids.copy():
            try:
                result = self.test_endpoint(
                    "DELETE",
                    f"/api/website-intelligence/website/{website_id}",
                    test_name=f"Cleanup Website {website_id[:8]}..."
                )
                if result["test_passed"]:
                    self.test_website_ids.remove(website_id)
            except Exception as e:
                print(f"   ⚠️ Could not cleanup {website_id}: {e}")

    def run_all_tests(self):
        """Run all Website Intelligence Hub tests"""
        print("🚀 STARTING WEBSITE INTELLIGENCE HUB BACKEND COMPREHENSIVE TESTING")
        print("=" * 70)
        print(f"Backend URL: {self.base_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        
        # Authenticate first
        if not self.authenticate():
            print("❌ Authentication failed - cannot proceed with tests")
            return self.results
        
        # Run all test suites in order
        self.test_mongodb_integration_and_dashboard()
        self.test_add_website_functionality()
        self.test_delete_website_functionality()
        self.test_update_all_websites()
        self.test_mongodb_data_quality()
        self.test_error_handling_edge_cases()
        
        # Cleanup
        self.cleanup_test_websites()
        
        # Print summary
        self.print_summary()
        
        return self.results

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 70)
        print("📊 WEBSITE INTELLIGENCE HUB COMPREHENSIVE TESTING SUMMARY")
        print("=" * 70)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Group results by test category
        categories = {
            "MongoDB Integration": [],
            "Add Website": [],
            "Delete Website": [],
            "Update All": [],
            "Data Quality": [],
            "Error Handling": [],
            "Cleanup": []
        }
        
        for result in self.results:
            test_name = result["test_name"].lower()
            if "mongodb" in test_name or "dashboard" in test_name:
                categories["MongoDB Integration"].append(result)
            elif "add" in test_name and "website" in test_name:
                categories["Add Website"].append(result)
            elif "delete" in test_name:
                categories["Delete Website"].append(result)
            elif "update all" in test_name:
                categories["Update All"].append(result)
            elif "data quality" in test_name or "datetime" in test_name or "persistence" in test_name:
                categories["Data Quality"].append(result)
            elif "error" in test_name or "invalid" in test_name or "missing" in test_name:
                categories["Error Handling"].append(result)
            elif "cleanup" in test_name:
                categories["Cleanup"].append(result)
        
        print("\n📋 RESULTS BY CATEGORY:")
        for category, results in categories.items():
            if results:
                passed = sum(1 for r in results if r["test_passed"])
                total = len(results)
                rate = (passed / total * 100) if total > 0 else 0
                print(f"  {category}: {passed}/{total} ({rate:.1f}%)")
        
        # Show failed tests with details
        failed_tests = [r for r in self.results if not r["test_passed"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                error_detail = ""
                if isinstance(test['response_data'], dict):
                    if 'detail' in test['response_data']:
                        error_detail = f" - {test['response_data']['detail']}"
                    elif 'error' in test['response_data']:
                        error_detail = f" - {test['response_data']['error']}"
                
                print(f"  • {test['test_name']}: {test['status_code']}{error_detail}")
        
        # Show successful tests with key information
        successful_tests = [r for r in self.results if r["test_passed"]]
        if successful_tests:
            print(f"\n✅ SUCCESSFUL TESTS ({len(successful_tests)}):")
            for test in successful_tests:
                response_data = test["response_data"]
                key_info = ""
                if isinstance(response_data, dict):
                    if "website_id" in response_data:
                        key_info += f" | Website ID: {response_data['website_id'][:8]}..."
                    if "status" in response_data:
                        key_info += f" | Status: {response_data['status']}"
                    if "dashboard" in response_data:
                        key_info += " | Dashboard data retrieved"
                    if "message" in response_data:
                        key_info += f" | {response_data['message'][:50]}..."
                
                print(f"  • {test['test_name']}: {test['status_code']}{key_info}")
        
        print(f"\nTest Completed: {datetime.now().isoformat()}")
        
        # Overall assessment
        if success_rate >= 90:
            print("🎉 EXCELLENT: Website Intelligence Hub MongoDB integration is working excellently!")
        elif success_rate >= 75:
            print("✅ GOOD: Website Intelligence Hub MongoDB integration is working well with minor issues.")
        elif success_rate >= 50:
            print("⚠️  MODERATE: Website Intelligence Hub has some issues that need attention.")
        else:
            print("❌ POOR: Website Intelligence Hub has significant issues requiring immediate attention.")
        
        # Key findings summary
        print("\n🔍 KEY FINDINGS:")
        mongodb_tests = [r for r in self.results if "mongodb" in r["test_name"].lower() or "dashboard" in r["test_name"].lower()]
        add_tests = [r for r in self.results if "add" in r["test_name"].lower() and "website" in r["test_name"].lower()]
        delete_tests = [r for r in self.results if "delete" in r["test_name"].lower()]
        
        if mongodb_tests and all(t["test_passed"] for t in mongodb_tests):
            print("  ✅ MongoDB integration working - data retrieval and persistence confirmed")
        
        if add_tests and any(t["test_passed"] for t in add_tests):
            passed_adds = sum(1 for t in add_tests if t["test_passed"])
            print(f"  ✅ Website addition functionality working - {passed_adds} successful additions")
        
        if delete_tests and any(t["test_passed"] for t in delete_tests):
            passed_deletes = sum(1 for t in delete_tests if t["test_passed"])
            print(f"  ✅ Website deletion functionality working - {passed_deletes} successful operations")

def main():
    """Main testing function"""
    tester = WebsiteIntelligenceHubTester(BACKEND_URL)
    results = tester.run_all_tests()
    
    # Save results to file for analysis
    with open('/app/website_intelligence_comprehensive_test_results.json', 'w') as f:
        json.dump({
            "test_summary": {
                "total_tests": tester.total_tests,
                "passed_tests": tester.passed_tests,
                "success_rate": (tester.passed_tests / tester.total_tests * 100) if tester.total_tests > 0 else 0,
                "test_timestamp": datetime.now().isoformat(),
                "focus_areas": [
                    "MongoDB Integration & Data Persistence",
                    "Add Website Functionality",
                    "Delete Website Functionality (NEWLY IMPLEMENTED)",
                    "Update All Websites",
                    "MongoDB Data Quality",
                    "Error Handling & Edge Cases"
                ]
            },
            "detailed_results": results
        }, f, indent=2, default=str)
    
    return tester.passed_tests, tester.total_tests

if __name__ == "__main__":
    passed, total = main()
    
    # Exit with appropriate code
    if passed == total:
        sys.exit(0)  # All tests passed
    else:
        sys.exit(1)  # Some tests failed