#!/usr/bin/env python3
"""
CustomerMind IQ - Affiliate Resources Backend Testing
Testing the new affiliate resources endpoints as requested in the review

SPECIFIC TEST OBJECTIVES:
1. **GET /api/affiliate/resources** - Test that this endpoint returns the list of affiliate resources including:
   - ROI Calculator
   - Customer IQ Articles  
   - FAQ Document
   - Verify the response includes download URLs, usage tips, categories, and metadata

2. **POST /api/affiliate/resources/{resource_id}/download** - Test the download tracking endpoint:
   - Test with resource_id "roi_calculator" 
   - Test with resource_id "customer_iq_articles"
   - Test with resource_id "faq_document"
   - Verify it tracks downloads properly and returns success responses

3. **Verify the existing affiliate system is still working** - Make sure the new endpoints didn't break existing functionality:
   - Test a few key existing endpoints like dashboard, generate-link, etc.

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

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://pagebuilder-iq.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class AffiliateResourcesTester:
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

    def test_affiliate_resources_endpoint(self) -> bool:
        """Test GET /api/affiliate/resources endpoint"""
        try:
            print("📋 Testing affiliate resources endpoint...")
            response = self.session.get(
                f"{API_BASE}/affiliate/resources",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                required_fields = ["success", "resources", "total_resources", "categories", "message"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Affiliate Resources Structure", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Check if we have the expected resources
                resources = data.get("resources", [])
                expected_resource_ids = ["roi_calculator", "customer_iq_articles", "faq_document"]
                
                found_resources = [r.get("id") for r in resources]
                missing_resources = [rid for rid in expected_resource_ids if rid not in found_resources]
                
                if missing_resources:
                    self.log_test("Affiliate Resources Content", False, f"Missing resources: {missing_resources}")
                    return False
                
                # Validate each resource has required fields
                resource_validation_passed = True
                for resource in resources:
                    required_resource_fields = ["id", "title", "description", "type", "file_type", "download_url", "category", "usage_tips"]
                    missing_resource_fields = [field for field in required_resource_fields if field not in resource]
                    
                    if missing_resource_fields:
                        self.log_test(f"Resource {resource.get('id', 'unknown')} Validation", False, f"Missing fields: {missing_resource_fields}")
                        resource_validation_passed = False
                
                if not resource_validation_passed:
                    return False
                
                # Check categories
                categories = data.get("categories", [])
                expected_categories = ["tools", "content", "support"]
                missing_categories = [cat for cat in expected_categories if cat not in categories]
                
                if missing_categories:
                    self.log_test("Affiliate Resources Categories", False, f"Missing categories: {missing_categories}")
                    return False
                
                self.log_test("Affiliate Resources Endpoint", True, 
                            f"Found {len(resources)} resources with all required fields and categories", data)
                return True
                
            else:
                self.log_test("Affiliate Resources Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Affiliate Resources Endpoint", False, f"Exception: {str(e)}")
            return False

    def test_resource_download_tracking(self) -> bool:
        """Test POST /api/affiliate/resources/{resource_id}/download endpoints"""
        try:
            print("📥 Testing resource download tracking...")
            
            resource_ids = ["roi_calculator", "customer_iq_articles", "faq_document"]
            all_tests_passed = True
            
            for resource_id in resource_ids:
                print(f"   Testing download tracking for: {resource_id}")
                
                # Test download tracking
                response = self.session.post(
                    f"{API_BASE}/affiliate/resources/{resource_id}/download",
                    json={"affiliate_id": "test_affiliate_123"},
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
            self.log_test("Resource Download Tracking", False, f"Exception: {str(e)}")
            return False

    def create_test_affiliate(self) -> str:
        """Create a test affiliate for testing purposes"""
        try:
            print("👤 Creating test affiliate...")
            
            test_affiliate_data = {
                "first_name": "Test",
                "last_name": "Affiliate",
                "email": f"test.affiliate.{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
                "phone": "+1-555-123-4567",
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
                json=test_affiliate_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                affiliate_id = data.get("affiliate_id")
                if affiliate_id:
                    self.log_test("Create Test Affiliate", True, f"Created affiliate: {affiliate_id}")
                    return affiliate_id
                else:
                    self.log_test("Create Test Affiliate", False, "No affiliate_id in response")
                    return None
            else:
                self.log_test("Create Test Affiliate", False, f"HTTP {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            self.log_test("Create Test Affiliate", False, f"Exception: {str(e)}")
            return None

    def test_existing_affiliate_endpoints(self) -> bool:
        """Test key existing affiliate endpoints to ensure they still work"""
        try:
            print("🔄 Testing existing affiliate system endpoints...")
            
            # First create a test affiliate
            test_affiliate_id = self.create_test_affiliate()
            if not test_affiliate_id:
                print("   Cannot test affiliate endpoints without a valid affiliate")
                return False
            
            # Test affiliate dashboard endpoint
            print("   Testing affiliate dashboard...")
            response = self.session.get(
                f"{API_BASE}/affiliate/dashboard",
                params={"affiliate_id": test_affiliate_id},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Affiliate Dashboard", True, "Dashboard endpoint working", data)
            else:
                self.log_test("Affiliate Dashboard", False, f"HTTP {response.status_code}: {response.text}")
                return False
            
            # Test generate link endpoint
            print("   Testing generate link...")
            response = self.session.post(
                f"{API_BASE}/affiliate/generate-link",
                params={"affiliate_id": test_affiliate_id},
                json={
                    "link_type": "trial",
                    "campaign_name": "test_campaign"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if "tracking_url" in data:
                    self.log_test("Generate Link", True, "Link generation working", data)
                else:
                    self.log_test("Generate Link", False, "Response missing tracking_url")
                    return False
            else:
                self.log_test("Generate Link", False, f"HTTP {response.status_code}: {response.text}")
                return False
            
            # Test materials endpoint
            print("   Testing materials endpoint...")
            response = self.session.get(
                f"{API_BASE}/affiliate/materials",
                params={"affiliate_id": test_affiliate_id},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Affiliate Materials", True, "Materials endpoint working", data)
            else:
                self.log_test("Affiliate Materials", False, f"HTTP {response.status_code}: {response.text}")
                return False
            
            return True
                
        except Exception as e:
            self.log_test("Existing Affiliate Endpoints", False, f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all affiliate resources tests"""
        print("🚀 Starting Affiliate Resources Backend Testing")
        print(f"🔗 Backend URL: {BACKEND_URL}")
        print(f"📡 API Base: {API_BASE}")
        print("=" * 80)
        
        # Step 1: Authenticate
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return False
        
        # Step 2: Test new affiliate resources endpoint
        resources_test_passed = self.test_affiliate_resources_endpoint()
        
        # Step 3: Test download tracking endpoints
        download_test_passed = self.test_resource_download_tracking()
        
        # Step 4: Test existing affiliate endpoints
        existing_test_passed = self.test_existing_affiliate_endpoints()
        
        # Summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(1 for result in self.test_results if result["success"])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if not resources_test_passed:
            print("❌ CRITICAL: Affiliate resources endpoint failed")
        
        if not download_test_passed:
            print("❌ CRITICAL: Download tracking endpoints failed")
        
        if not existing_test_passed:
            print("❌ CRITICAL: Existing affiliate endpoints failed")
        
        if resources_test_passed and download_test_passed and existing_test_passed:
            print("🎉 ALL AFFILIATE RESOURCES TESTS PASSED!")
            print("✅ New affiliate resources endpoints are working correctly")
            print("✅ Download tracking is functional")
            print("✅ Existing affiliate system remains operational")
        else:
            print("⚠️  Some tests failed - see details above")
        
        print("\n📋 Detailed Test Results:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
        
        return resources_test_passed and download_test_passed and existing_test_passed

def main():
    """Main test execution"""
    tester = AffiliateResourcesTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎯 CONCLUSION: Affiliate resources functionality is working correctly!")
        sys.exit(0)
    else:
        print("\n💥 CONCLUSION: Some affiliate resources tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()