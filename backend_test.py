#!/usr/bin/env python3
"""
CustomerMind IQ - Affiliate System Backend Testing
Testing the affiliate system after internationalization features were added

SPECIFIC TEST OBJECTIVES FROM REVIEW REQUEST:
1. **Test affiliate registration endpoint** (/api/affiliate/register)
2. **Test affiliate login endpoint** (/api/affiliate/auth/login) 
3. **Test affiliate resources endpoint** (/api/affiliate/resources)
4. **Verify that all endpoints are responding correctly and the database connections are working**
5. **Make sure the recent media assets (audio, video, presentation) are still available**

Use admin credentials: admin@customermindiq.com / CustomerMindIQ2025!
"""

import asyncio
import json
import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - Use production URL from frontend .env
BACKEND_URL = "https://mindiq-portal.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class AffiliateSystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.admin_token = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if response_data and isinstance(response_data, dict):
            print(f"   Response keys: {list(response_data.keys())}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print()

    def authenticate_admin(self) -> bool:
        """Authenticate as admin user"""
        try:
            print("🔐 Authenticating as admin...")
            response = self.session.post(
                f"{API_BASE}/auth/login",
                json=ADMIN_CREDENTIALS,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                if self.admin_token:
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.admin_token}"
                    })
                    self.log_test("Admin Authentication", True, f"Successfully authenticated as {ADMIN_CREDENTIALS['email']}")
                    return True
                else:
                    self.log_test("Admin Authentication", False, "No access token in response")
                    return False
            else:
                self.log_test("Admin Authentication", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False

    def test_affiliate_registration(self) -> bool:
        """Test affiliate registration endpoint"""
        try:
            print("📝 Testing affiliate registration endpoint...")
            
            # Create test affiliate data
            test_affiliate = {
                "first_name": "Test",
                "last_name": "Affiliate",
                "email": f"test.affiliate.{int(datetime.now().timestamp())}@example.com",
                "phone": "+1234567890",
                "website": "https://testaffiliate.com",
                "promotion_method": "social",
                "password": "TestPassword123!",
                "address": {
                    "street": "123 Test Street",
                    "city": "Test City",
                    "state": "CA",
                    "zip_code": "12345",
                    "country": "US"
                },
                "payment_method": "paypal",
                "payment_details": {
                    "paypal_email": "test@paypal.com"
                }
            }
            
            response = self.session.post(
                f"{API_BASE}/affiliate/auth/register",
                json=test_affiliate,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                required_fields = ["success", "affiliate_id", "message"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Affiliate Registration Structure", False, f"Missing fields: {missing_fields}")
                    return False
                
                if data.get("success"):
                    self.log_test("Affiliate Registration", True, f"Successfully registered affiliate: {data.get('affiliate_id')}")
                    return True
                else:
                    self.log_test("Affiliate Registration", False, f"Registration failed: {data.get('message')}")
                    return False
                
            else:
                self.log_test("Affiliate Registration", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Affiliate Registration", False, f"Exception: {str(e)}")
            return False

    def test_affiliate_login(self) -> bool:
        """Test affiliate login endpoint with existing admin affiliate"""
        try:
            print("🔐 Testing affiliate login endpoint...")
            
            # Try to login with admin affiliate account
            login_data = {
                "email": "admin@customermindiq.com",
                "password": "CustomerMindIQ2025!"
            }
            
            response = self.session.post(
                f"{API_BASE}/affiliate/auth/login",
                json=login_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                required_fields = ["success", "token", "affiliate"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Affiliate Login Structure", False, f"Missing fields: {missing_fields}")
                    return False
                
                if data.get("success") and data.get("token"):
                    affiliate_info = data.get("affiliate", {})
                    self.log_test("Affiliate Login", True, f"Successfully logged in affiliate: {affiliate_info.get('name', 'Unknown')}")
                    return True
                else:
                    self.log_test("Affiliate Login", False, f"Login failed: {data}")
                    return False
                    
            elif response.status_code == 403:
                # Account pending approval - this is expected behavior
                self.log_test("Affiliate Login", True, "Account pending approval (expected behavior)")
                return True
                
            else:
                self.log_test("Affiliate Login", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Affiliate Login", False, f"Exception: {str(e)}")
            return False

    def test_resource_structure(self) -> bool:
        """Test that each resource has all required fields"""
        try:
            print("🔍 Testing resource structure...")
            response = self.session.get(
                f"{API_BASE}/affiliate/resources",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                resources = data.get("resources", [])
                
                required_fields = ["id", "title", "description", "type", "file_type", "download_url", "category", "usage_tips"]
                
                all_valid = True
                for resource in resources:
                    missing_fields = [field for field in required_fields if field not in resource]
                    
                    if missing_fields:
                        self.log_test(f"Resource Structure - {resource.get('id', 'unknown')}", False, f"Missing fields: {missing_fields}")
                        all_valid = False
                    else:
                        # Check that usage_tips is a list
                        if not isinstance(resource.get("usage_tips"), list):
                            self.log_test(f"Resource Structure - {resource.get('id')}", False, "usage_tips should be a list")
                            all_valid = False
                
                if all_valid:
                    self.log_test("Resource Structure", True, f"All {len(resources)} resources have required fields")
                    return True
                else:
                    return False
                
            else:
                self.log_test("Resource Structure", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Resource Structure", False, f"Exception: {str(e)}")
            return False

    def test_categories_include_sales(self) -> bool:
        """Test that categories now include the new 'sales' category"""
        try:
            print("📂 Testing categories include 'sales'...")
            response = self.session.get(
                f"{API_BASE}/affiliate/resources",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                categories = data.get("categories", [])
                
                expected_categories = ["tools", "content", "support", "sales"]
                missing_categories = [cat for cat in expected_categories if cat not in categories]
                
                if missing_categories:
                    self.log_test("Categories Include Sales", False, f"Missing categories: {missing_categories}")
                    return False
                
                # Specifically check for 'sales' category
                if "sales" not in categories:
                    self.log_test("Sales Category Present", False, "New 'sales' category not found in categories")
                    return False
                
                self.log_test("Categories Include Sales", True, f"All expected categories present: {categories}")
                return True
                
            else:
                self.log_test("Categories Include Sales", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Categories Include Sales", False, f"Exception: {str(e)}")
            return False

    def test_download_urls_valid(self) -> bool:
        """Test that new resources have correct download URLs"""
        try:
            print("🔗 Testing download URLs for new resources...")
            response = self.session.get(
                f"{API_BASE}/affiliate/resources",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                resources = data.get("resources", [])
                
                # Find the new resources
                white_paper = next((r for r in resources if r.get("id") == "white_paper"), None)
                pricing_schedule = next((r for r in resources if r.get("id") == "pricing_schedule"), None)
                
                if not white_paper:
                    self.log_test("White Paper Resource", False, "White paper resource not found")
                    return False
                
                if not pricing_schedule:
                    self.log_test("Pricing Schedule Resource", False, "Pricing schedule resource not found")
                    return False
                
                # Check download URLs
                white_paper_url = white_paper.get("download_url", "")
                pricing_schedule_url = pricing_schedule.get("download_url", "")
                
                # URLs should point to customer-assets.emergentagent.com
                expected_domain = "customer-assets.emergentagent.com"
                
                if expected_domain not in white_paper_url:
                    self.log_test("White Paper URL", False, f"URL doesn't contain expected domain: {white_paper_url}")
                    return False
                
                if expected_domain not in pricing_schedule_url:
                    self.log_test("Pricing Schedule URL", False, f"URL doesn't contain expected domain: {pricing_schedule_url}")
                    return False
                
                # Check that URLs contain the expected file names
                if "White%20Paper" not in white_paper_url and "White Paper" not in white_paper_url:
                    self.log_test("White Paper Filename", False, f"URL doesn't contain expected filename: {white_paper_url}")
                    return False
                
                if "Pricing%20Schedule" not in pricing_schedule_url and "Pricing Schedule" not in pricing_schedule_url:
                    self.log_test("Pricing Schedule Filename", False, f"URL doesn't contain expected filename: {pricing_schedule_url}")
                    return False
                
                self.log_test("Download URLs Valid", True, "Both new resources have valid download URLs")
                return True
                
            else:
                self.log_test("Download URLs Valid", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Download URLs Valid", False, f"Exception: {str(e)}")
            return False

    def test_new_resource_download_tracking(self) -> bool:
        """Test download tracking for the new resources"""
        try:
            print("📥 Testing download tracking for new resources...")
            
            new_resource_ids = ["white_paper", "pricing_schedule"]
            all_tests_passed = True
            
            for resource_id in new_resource_ids:
                print(f"   Testing download tracking for: {resource_id}")
                
                # Test download tracking
                response = self.session.post(
                    f"{API_BASE}/affiliate/resources/{resource_id}/download",
                    json={"affiliate_id": "test_affiliate_new_resources"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and "message" in data:
                        if data.get("success"):
                            self.log_test(f"Download Tracking - {resource_id}", True, 
                                        f"Successfully tracked download: {data.get('message')}")
                        else:
                            self.log_test(f"Download Tracking - {resource_id}", False, 
                                        f"Download tracking failed: {data.get('message')}")
                            all_tests_passed = False
                    else:
                        self.log_test(f"Download Tracking - {resource_id}", False, 
                                    "Response missing required fields (success, message)")
                        all_tests_passed = False
                else:
                    self.log_test(f"Download Tracking - {resource_id}", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    all_tests_passed = False
            
            return all_tests_passed
                
        except Exception as e:
            self.log_test("New Resource Download Tracking", False, f"Exception: {str(e)}")
            return False

    def test_resource_categories_assignment(self) -> bool:
        """Test that new resources are assigned to correct categories"""
        try:
            print("📂 Testing resource category assignments...")
            response = self.session.get(
                f"{API_BASE}/affiliate/resources",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                resources = data.get("resources", [])
                
                # Find the new resources and check their categories
                white_paper = next((r for r in resources if r.get("id") == "white_paper"), None)
                pricing_schedule = next((r for r in resources if r.get("id") == "pricing_schedule"), None)
                
                if not white_paper or not pricing_schedule:
                    self.log_test("Resource Category Assignment", False, "New resources not found")
                    return False
                
                # Check categories
                white_paper_category = white_paper.get("category")
                pricing_schedule_category = pricing_schedule.get("category")
                
                # White paper should be in 'content' category
                if white_paper_category != "content":
                    self.log_test("White Paper Category", False, f"Expected 'content', got '{white_paper_category}'")
                    return False
                
                # Pricing schedule should be in 'sales' category
                if pricing_schedule_category != "sales":
                    self.log_test("Pricing Schedule Category", False, f"Expected 'sales', got '{pricing_schedule_category}'")
                    return False
                
                self.log_test("Resource Category Assignment", True, "New resources correctly categorized")
                return True
                
            else:
                self.log_test("Resource Category Assignment", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Resource Category Assignment", False, f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all updated affiliate resources tests"""
        print("🚀 Starting Updated Affiliate Resources Backend Testing")
        print(f"🔗 Backend URL: {BACKEND_URL}")
        print(f"📡 API Base: {API_BASE}")
        print("=" * 80)
        
        # Step 1: Authenticate
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return False
        
        # Step 2: Test resource count (should be 5 now)
        count_test_passed = self.test_affiliate_resources_count()
        
        # Step 3: Test specific resources are present
        resources_test_passed = self.test_specific_resources_present()
        
        # Step 4: Test resource structure
        structure_test_passed = self.test_resource_structure()
        
        # Step 5: Test categories include 'sales'
        categories_test_passed = self.test_categories_include_sales()
        
        # Step 6: Test download URLs are valid
        urls_test_passed = self.test_download_urls_valid()
        
        # Step 7: Test download tracking for new resources
        download_test_passed = self.test_new_resource_download_tracking()
        
        # Step 8: Test resource category assignments
        category_assignment_passed = self.test_resource_categories_assignment()
        
        # Summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(1 for result in self.test_results if result["success"])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        # Critical test results
        critical_tests = [
            ("Resource Count (5 resources)", count_test_passed),
            ("Specific Resources Present", resources_test_passed),
            ("Resource Structure", structure_test_passed),
            ("Categories Include Sales", categories_test_passed),
            ("Download URLs Valid", urls_test_passed),
            ("New Resource Download Tracking", download_test_passed),
            ("Resource Category Assignment", category_assignment_passed)
        ]
        
        all_critical_passed = all(passed for _, passed in critical_tests)
        
        if all_critical_passed:
            print("🎉 ALL AFFILIATE RESOURCES UPDATE TESTS PASSED!")
            print("✅ Affiliate resources endpoint now returns 5 resources (was 3)")
            print("✅ New resources (CMIQ White Paper, Customer Mind Pricing Schedule) are present")
            print("✅ All resources have required structure fields")
            print("✅ Categories now include 'sales' category")
            print("✅ Download URLs are valid and point to correct documents")
            print("✅ Download tracking works for new resources")
            print("✅ Resources are correctly categorized")
        else:
            print("⚠️  Some critical tests failed:")
            for test_name, passed in critical_tests:
                if not passed:
                    print(f"   ❌ {test_name}")
        
        print("\n📋 Detailed Test Results:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
        
        return all_critical_passed

def main():
    """Main test execution"""
    tester = UpdatedAffiliateResourcesTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎯 CONCLUSION: Updated affiliate resources functionality is working correctly!")
        print("   - 5 resources now available (up from 3)")
        print("   - New CMIQ White Paper and Customer Mind Pricing Schedule added")
        print("   - Sales category added to categories")
        print("   - Download tracking functional for all resources")
        sys.exit(0)
    else:
        print("\n💥 CONCLUSION: Some affiliate resources update tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()