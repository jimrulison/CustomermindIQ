#!/usr/bin/env python3
"""
Website Intelligence Hub Data Persistence Backend Test

URGENT: Debug critical data persistence issue where user reports:
- After deleting websites and adding new ones
- When they refresh the page, old websites come back and new ones disappear
- This suggests MongoDB persistence isn't working correctly

This test focuses on the real user scenario using localhost backend.
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, Any, List

# Use localhost for testing
BACKEND_URL = "http://localhost:8001"

print(f"🔗 Testing Website Intelligence Hub Data Persistence at: {BACKEND_URL}")
print(f"🚨 URGENT: Debugging critical data persistence issue")

class WebsiteIntelligenceDataPersistenceTest:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.user_added_websites = []  # Track websites we add during testing
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
    
    def make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request and return response data"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            try:
                response_data = response.json()
            except:
                response_data = {"error": "Invalid JSON response", "text": response.text[:500]}
            
            return {
                "status_code": response.status_code,
                "data": response_data,
                "success": 200 <= response.status_code < 300
            }
            
        except Exception as e:
            return {
                "status_code": 0,
                "data": {"error": str(e)},
                "success": False
            }

    def test_1_check_mongodb_connection(self):
        """Test 1: Check MongoDB connection and database state"""
        print("\n🔍 TEST 1: CHECK MONGODB CONNECTION AND DATABASE STATE")
        print("=" * 60)
        
        # Test database connection via health endpoint
        response = self.make_request("GET", "/api/test-db")
        
        if response["success"]:
            db_data = response["data"]
            connection_status = db_data.get("connection", "Unknown")
            read_permission = db_data.get("read_permission", "Unknown")
            write_permission = db_data.get("write_permission", "Unknown")
            
            self.log_test(
                "MongoDB Connection Test",
                "PASS" if "SUCCESS" in connection_status else "FAIL",
                f"Connection: {connection_status}, Read: {read_permission}, Write: {write_permission}"
            )
        else:
            self.log_test(
                "MongoDB Connection Test",
                "FAIL",
                f"Database test endpoint failed: {response['data']}"
            )

    def test_2_initial_dashboard_state(self):
        """Test 2: Check initial dashboard state and existing websites"""
        print("\n🔍 TEST 2: CHECK INITIAL DASHBOARD STATE")
        print("=" * 60)
        
        response = self.make_request("GET", "/api/website-intelligence/dashboard")
        
        if response["success"]:
            dashboard_data = response["data"]
            user_websites = dashboard_data.get("dashboard", {}).get("user_websites", [])
            
            # Count static vs user-added websites
            static_websites = [w for w in user_websites if w.get("website_id", "").startswith("web_")]
            user_added_websites = [w for w in user_websites if not w.get("website_id", "").startswith("web_")]
            
            self.log_test(
                "Initial Dashboard State",
                "PASS",
                f"Total websites: {len(user_websites)}, Static: {len(static_websites)}, User-added: {len(user_added_websites)}"
            )
            
            # Log current user-added websites for tracking
            print(f"   📋 Current websites in dashboard:")
            for website in user_websites:
                website_type = "STATIC" if website.get("website_id", "").startswith("web_") else "USER-ADDED"
                print(f"      • {website.get('website_name', 'Unknown')} ({website.get('domain', 'Unknown')}) - {website_type} - ID: {website.get('website_id', 'Unknown')}")
            
            return user_websites
        else:
            self.log_test(
                "Initial Dashboard State",
                "FAIL",
                f"Dashboard endpoint failed: {response['data']}"
            )
            return []

    def test_3_add_new_website(self):
        """Test 3: Add a new website and verify it's stored in MongoDB"""
        print("\n🔍 TEST 3: ADD NEW WEBSITE AND VERIFY MONGODB STORAGE")
        print("=" * 60)
        
        # Add a realistic website with current timestamp to make it unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_website = {
            "domain": f"testpersistence_{timestamp}.com",
            "name": f"Test Persistence Website {timestamp}",
            "type": "E-commerce",
            "membership_tier": "professional",
            "current_websites": 2
        }
        
        response = self.make_request("POST", "/api/website-intelligence/website/add", test_website)
        
        if response["success"]:
            website_data = response["data"]
            website_id = website_data.get("website_id")
            
            if website_id:
                self.user_added_websites.append(website_id)
                self.log_test(
                    "Add New Website",
                    "PASS",
                    f"Website added successfully - ID: {website_id}, Name: {test_website['name']}"
                )
                
                # Immediately check if it appears in dashboard
                time.sleep(1)  # Brief pause
                dashboard_response = self.make_request("GET", "/api/website-intelligence/dashboard")
                
                if dashboard_response["success"]:
                    dashboard_data = dashboard_response["data"]
                    user_websites = dashboard_data.get("dashboard", {}).get("user_websites", [])
                    
                    # Check if our new website is in the dashboard
                    new_website_found = any(w.get("website_id") == website_id for w in user_websites)
                    
                    self.log_test(
                        "New Website in Dashboard",
                        "PASS" if new_website_found else "FAIL",
                        f"Website {'found' if new_website_found else 'NOT FOUND'} in dashboard after adding"
                    )
                    
                    return website_id
                else:
                    self.log_test(
                        "New Website in Dashboard",
                        "FAIL",
                        "Could not retrieve dashboard after adding website"
                    )
            else:
                self.log_test(
                    "Add New Website",
                    "FAIL",
                    "No website_id returned from add website endpoint"
                )
        else:
            self.log_test(
                "Add New Website",
                "FAIL",
                f"Add website failed: {response['data']}"
            )
        
        return None

    def test_4_simulate_page_refresh(self, added_website_id: str = None):
        """Test 4: Simulate page refresh by calling dashboard again"""
        print("\n🔍 TEST 4: SIMULATE PAGE REFRESH (DASHBOARD RELOAD)")
        print("=" * 60)
        
        if not added_website_id:
            self.log_test(
                "Page Refresh Simulation",
                "SKIP",
                "No website ID to test with"
            )
            return
        
        # Wait a moment to simulate real user behavior
        time.sleep(2)
        
        # Call dashboard again (simulating page refresh)
        response = self.make_request("GET", "/api/website-intelligence/dashboard")
        
        if response["success"]:
            dashboard_data = response["data"]
            user_websites = dashboard_data.get("dashboard", {}).get("user_websites", [])
            
            # Check if our added website is still there
            website_still_present = any(w.get("website_id") == added_website_id for w in user_websites)
            
            self.log_test(
                "Website Persistence After Refresh",
                "PASS" if website_still_present else "FAIL",
                f"Added website {'still present' if website_still_present else 'DISAPPEARED'} after page refresh"
            )
            
            # Log all current websites for debugging
            print(f"   📋 Current websites after refresh:")
            for website in user_websites:
                website_type = "STATIC" if website.get("website_id", "").startswith("web_") else "USER-ADDED"
                print(f"      • {website.get('website_name', 'Unknown')} ({website.get('domain', 'Unknown')}) - {website_type} - ID: {website.get('website_id', 'Unknown')}")
            
        else:
            self.log_test(
                "Website Persistence After Refresh",
                "FAIL",
                f"Dashboard failed after refresh: {response['data']}"
            )

    def test_5_delete_website_functionality(self, website_id_to_delete: str = None):
        """Test 5: Test delete functionality and verify removal from MongoDB"""
        print("\n🔍 TEST 5: TEST DELETE FUNCTIONALITY")
        print("=" * 60)
        
        if not website_id_to_delete:
            self.log_test(
                "Delete Website Test",
                "SKIP",
                "No website ID to delete"
            )
            return
        
        # First, verify the website exists
        dashboard_response = self.make_request("GET", "/api/website-intelligence/dashboard")
        if dashboard_response["success"]:
            user_websites = dashboard_response["data"].get("dashboard", {}).get("user_websites", [])
            website_exists = any(w.get("website_id") == website_id_to_delete for w in user_websites)
            
            if not website_exists:
                self.log_test(
                    "Delete Website Test",
                    "FAIL",
                    f"Website {website_id_to_delete} not found before deletion attempt"
                )
                return
        
        # Attempt to delete the website
        response = self.make_request("DELETE", f"/api/website-intelligence/website/{website_id_to_delete}")
        
        if response["success"]:
            delete_data = response["data"]
            self.log_test(
                "Delete Website Request",
                "PASS",
                f"Delete request successful: {delete_data.get('message', 'No message')}"
            )
            
            # Verify deletion by checking dashboard
            time.sleep(1)  # Brief pause
            dashboard_response = self.make_request("GET", "/api/website-intelligence/dashboard")
            
            if dashboard_response["success"]:
                user_websites = dashboard_response["data"].get("dashboard", {}).get("user_websites", [])
                website_still_exists = any(w.get("website_id") == website_id_to_delete for w in user_websites)
                
                self.log_test(
                    "Website Removal Verification",
                    "PASS" if not website_still_exists else "FAIL",
                    f"Website {'successfully removed' if not website_still_exists else 'STILL EXISTS'} from dashboard"
                )
            else:
                self.log_test(
                    "Website Removal Verification",
                    "FAIL",
                    "Could not verify deletion - dashboard request failed"
                )
        else:
            self.log_test(
                "Delete Website Request",
                "FAIL",
                f"Delete request failed: {response['data']}"
            )

    def test_6_simulate_refresh_after_delete(self):
        """Test 6: Simulate page refresh after deletion to check if deleted website reappears"""
        print("\n🔍 TEST 6: SIMULATE REFRESH AFTER DELETION")
        print("=" * 60)
        
        # Wait to simulate real user behavior
        time.sleep(2)
        
        # Call dashboard again
        response = self.make_request("GET", "/api/website-intelligence/dashboard")
        
        if response["success"]:
            dashboard_data = response["data"]
            user_websites = dashboard_data.get("dashboard", {}).get("user_websites", [])
            
            # Check if any of our test websites reappeared
            reappeared_websites = []
            for website_id in self.user_added_websites:
                if any(w.get("website_id") == website_id for w in user_websites):
                    reappeared_websites.append(website_id)
            
            self.log_test(
                "Deleted Website Reappearance Check",
                "PASS" if not reappeared_websites else "FAIL",
                f"{'No deleted websites reappeared' if not reappeared_websites else f'DELETED WEBSITES REAPPEARED: {reappeared_websites}'}"
            )
            
            # Log final state
            print(f"   📋 Final website state:")
            for website in user_websites:
                website_type = "STATIC" if website.get("website_id", "").startswith("web_") else "USER-ADDED"
                print(f"      • {website.get('website_name', 'Unknown')} ({website.get('domain', 'Unknown')}) - {website_type} - ID: {website.get('website_id', 'Unknown')}")
            
        else:
            self.log_test(
                "Deleted Website Reappearance Check",
                "FAIL",
                f"Dashboard failed: {response['data']}"
            )

    def test_7_real_user_scenario(self):
        """Test 7: Simulate the exact user scenario reported"""
        print("\n🔍 TEST 7: REAL USER SCENARIO - EXACT ISSUE REPRODUCTION")
        print("=" * 60)
        
        # Step 1: Add multiple websites like a real user would
        test_websites = [
            {
                "domain": "realuser1.com",
                "name": "Real User Site 1",
                "type": "Blog",
                "membership_tier": "professional",
                "current_websites": 3
            },
            {
                "domain": "realuser2.com", 
                "name": "Real User Site 2",
                "type": "Corporate",
                "membership_tier": "professional",
                "current_websites": 4
            }
        ]
        
        added_website_ids = []
        
        print("   Step 1: Adding multiple websites...")
        for i, website_data in enumerate(test_websites):
            response = self.make_request("POST", "/api/website-intelligence/website/add", website_data)
            
            if response["success"]:
                website_id = response["data"].get("website_id")
                if website_id:
                    added_website_ids.append(website_id)
                    self.user_added_websites.append(website_id)
                    print(f"      ✅ Added website {i+1}: {website_data['name']} - ID: {website_id}")
                else:
                    print(f"      ❌ Failed to get ID for website {i+1}")
            else:
                print(f"      ❌ Failed to add website {i+1}: {response['data']}")
        
        # Step 2: Verify they appear in dashboard
        print("   Step 2: Verifying websites appear in dashboard...")
        dashboard_response = self.make_request("GET", "/api/website-intelligence/dashboard")
        if dashboard_response["success"]:
            user_websites = dashboard_response["data"].get("dashboard", {}).get("user_websites", [])
            websites_found = sum(1 for website_id in added_website_ids if any(w.get("website_id") == website_id for w in user_websites))
            print(f"      📊 Found {websites_found}/{len(added_website_ids)} newly added websites in dashboard")
        
        # Step 3: Delete some websites
        print("   Step 3: Deleting websites...")
        deleted_website_ids = []
        for website_id in added_website_ids[:1]:  # Delete first website
            response = self.make_request("DELETE", f"/api/website-intelligence/website/{website_id}")
            if response["success"]:
                deleted_website_ids.append(website_id)
                print(f"      ✅ Deleted website: {website_id}")
            else:
                print(f"      ❌ Failed to delete website: {website_id}")
        
        # Step 4: Verify deletion
        print("   Step 4: Verifying deletion...")
        dashboard_response = self.make_request("GET", "/api/website-intelligence/dashboard")
        if dashboard_response["success"]:
            user_websites = dashboard_response["data"].get("dashboard", {}).get("user_websites", [])
            deleted_still_present = sum(1 for website_id in deleted_website_ids if any(w.get("website_id") == website_id for w in user_websites))
            print(f"      📊 {deleted_still_present}/{len(deleted_website_ids)} deleted websites still present (should be 0)")
        
        # Step 5: Simulate page refresh (the critical test)
        print("   Step 5: Simulating page refresh (CRITICAL TEST)...")
        time.sleep(3)  # Simulate user taking time
        dashboard_response = self.make_request("GET", "/api/website-intelligence/dashboard")
        
        if dashboard_response["success"]:
            user_websites = dashboard_response["data"].get("dashboard", {}).get("user_websites", [])
            
            # Check if deleted websites reappeared
            deleted_reappeared = sum(1 for website_id in deleted_website_ids if any(w.get("website_id") == website_id for w in user_websites))
            
            # Check if remaining websites disappeared
            remaining_website_ids = [wid for wid in added_website_ids if wid not in deleted_website_ids]
            remaining_disappeared = sum(1 for website_id in remaining_website_ids if not any(w.get("website_id") == website_id for w in user_websites))
            
            # This is the critical test - reproducing the exact user issue
            critical_issue_detected = deleted_reappeared > 0 or remaining_disappeared > 0
            
            self.log_test(
                "Critical User Issue Reproduction",
                "FAIL" if critical_issue_detected else "PASS",
                f"Deleted reappeared: {deleted_reappeared}, Remaining disappeared: {remaining_disappeared}"
            )
            
            if critical_issue_detected:
                print(f"      🚨 CRITICAL ISSUE REPRODUCED!")
                print(f"         - Deleted websites that reappeared: {deleted_reappeared}")
                print(f"         - Remaining websites that disappeared: {remaining_disappeared}")
            else:
                print(f"      ✅ No critical issue detected - data persistence working correctly")
        
        return len(added_website_ids) == len(test_websites)

    def run_comprehensive_test(self):
        """Run comprehensive data persistence debugging test"""
        print("🚨 STARTING WEBSITE INTELLIGENCE HUB DATA PERSISTENCE DEBUGGING")
        print("=" * 80)
        print(f"Backend URL: {self.base_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("\nThis test debugs the critical issue where:")
        print("- User adds websites, they appear")
        print("- User deletes websites, they disappear") 
        print("- User refreshes page, old websites come back, new ones disappear")
        print("=" * 80)
        
        # Test 1: Check MongoDB connection
        self.test_1_check_mongodb_connection()
        
        # Test 2: Check initial state
        initial_websites = self.test_2_initial_dashboard_state()
        
        # Test 3: Add new website
        added_website_id = self.test_3_add_new_website()
        
        # Test 4: Simulate page refresh
        self.test_4_simulate_page_refresh(added_website_id)
        
        # Test 5: Delete website
        self.test_5_delete_website_functionality(added_website_id)
        
        # Test 6: Simulate refresh after delete
        self.test_6_simulate_refresh_after_delete()
        
        # Test 7: Real user scenario (most important)
        self.test_7_real_user_scenario()
        
        # Print summary
        self.print_summary()
        
        return self.results

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 WEBSITE INTELLIGENCE HUB DATA PERSISTENCE DEBUG SUMMARY")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Show failed tests
        failed_tests = [r for r in self.results if r["status"] == "FAIL"]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test_name']}: {test['details']}")
        
        # Show successful tests
        successful_tests = [r for r in self.results if r["status"] == "PASS"]
        if successful_tests:
            print(f"\n✅ SUCCESSFUL TESTS ({len(successful_tests)}):")
            for test in successful_tests:
                print(f"  • {test['test_name']}: {test['details']}")
        
        print(f"\nTest Completed: {datetime.now().isoformat()}")
        
        # Critical assessment for data persistence
        critical_issues = []
        
        for result in self.results:
            if result["status"] == "FAIL":
                if "reappeared" in result["details"].lower():
                    critical_issues.append("🚨 CRITICAL: Deleted websites reappearing after refresh")
                elif "disappeared" in result["details"].lower():
                    critical_issues.append("🚨 CRITICAL: Added websites disappearing after refresh")
                elif "mongodb" in result["test_name"].lower() and result["status"] == "FAIL":
                    critical_issues.append("🚨 CRITICAL: MongoDB connection/persistence issues")
                elif "critical user issue reproduction" in result["test_name"].lower():
                    critical_issues.append("🚨 CRITICAL: User-reported issue successfully reproduced")
        
        if critical_issues:
            print("\n🚨 CRITICAL DATA PERSISTENCE ISSUES IDENTIFIED:")
            for issue in critical_issues:
                print(f"   {issue}")
            print("\n💡 RECOMMENDED ACTIONS:")
            print("   1. Check MongoDB connection and write permissions")
            print("   2. Verify user_websites collection is being used correctly")
            print("   3. Check if dashboard is properly combining static + user data")
            print("   4. Investigate potential caching issues")
            print("   5. Verify delete operations are actually removing from MongoDB")
        else:
            print("\n✅ No critical data persistence issues detected in testing")
            print("   The MongoDB persistence system appears to be working correctly")

def main():
    """Main testing function"""
    tester = WebsiteIntelligenceDataPersistenceTest(BACKEND_URL)
    results = tester.run_comprehensive_test()
    
    # Save results to file for analysis
    with open('/app/website_intelligence_data_persistence_debug_results.json', 'w') as f:
        json.dump({
            "debug_summary": {
                "total_tests": tester.total_tests,
                "passed_tests": tester.passed_tests,
                "success_rate": (tester.passed_tests / tester.total_tests * 100) if tester.total_tests > 0 else 0,
                "test_timestamp": datetime.now().isoformat(),
                "critical_issue": "Data persistence debugging for user-reported issue"
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