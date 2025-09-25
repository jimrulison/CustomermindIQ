#!/usr/bin/env python3
"""
Email Platform Integrations System - Comprehensive Backend Testing
Testing all endpoints as specified in the review request
"""

import asyncio
import httpx
import json
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customeriq-hub.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials for testing
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

# Test data as specified in review request
TEST_AFFILIATE_ID = "test_affiliate_001"
CONVERTKIT_API_SECRET = "placeholder_convertkit_secret"
GETRESPONSE_API_KEY = "placeholder_getresponse_key"
ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/123456/test"
TEST_CUSTOMER_EMAIL = "test@example.com"
CONVERSION_VALUE = 97.00

class EmailIntegrationsTestSuite:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.admin_token = None
        self.test_results = []
        self.integration_ids = {}
        
    async def authenticate_admin(self):
        """Authenticate as admin user"""
        try:
            response = await self.client.post(f"{API_BASE}/auth/login", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                self.log_result("✅ Admin Authentication", True, f"Successfully authenticated admin user")
                return True
            else:
                self.log_result("❌ Admin Authentication", False, f"Failed with status {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("❌ Admin Authentication", False, f"Exception: {str(e)}")
            return False
    
    def get_auth_headers(self):
        """Get authorization headers"""
        if self.admin_token:
            return {"Authorization": f"Bearer {self.admin_token}"}
        return {}
    
    def log_result(self, test_name, success, details):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"{status}: {test_name} - {details}")
    
    async def test_health_check(self):
        """Test integration health check endpoint"""
        try:
            response = await self.client.get(f"{API_BASE}/integrations/health")
            
            if response.status_code == 200:
                data = response.json()
                platforms = data.get("platforms_supported", [])
                expected_platforms = ["convertkit", "getresponse", "zapier"]
                
                if all(platform in platforms for platform in expected_platforms):
                    self.log_result("Health Check", True, f"All platforms supported: {platforms}")
                else:
                    self.log_result("Health Check", False, f"Missing platforms. Got: {platforms}")
            else:
                self.log_result("Health Check", False, f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Health Check", False, f"Exception: {str(e)}")
    
    async def test_setup_convertkit_integration(self):
        """Test ConvertKit integration setup"""
        try:
            payload = {
                "affiliate_id": TEST_AFFILIATE_ID,
                "platform": "convertkit",
                "api_key": CONVERTKIT_API_SECRET,
                "tags": ["affiliate", "customer"],
                "custom_fields": {"source": "affiliate_program"}
            }
            
            response = await self.client.post(f"{API_BASE}/integrations/setup", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.integration_ids["convertkit"] = data.get("integration_id")
                    self.log_result("ConvertKit Setup", True, f"Integration ID: {data.get('integration_id')}")
                else:
                    self.log_result("ConvertKit Setup", False, f"Setup failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_result("ConvertKit Setup", False, f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("ConvertKit Setup", False, f"Exception: {str(e)}")
    
    async def test_setup_getresponse_integration(self):
        """Test GetResponse integration setup"""
        try:
            payload = {
                "affiliate_id": TEST_AFFILIATE_ID,
                "platform": "getresponse",
                "api_key": GETRESPONSE_API_KEY,
                "tags": ["affiliate", "customer"],
                "custom_fields": {"source": "affiliate_program"}
            }
            
            response = await self.client.post(f"{API_BASE}/integrations/setup", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.integration_ids["getresponse"] = data.get("integration_id")
                    self.log_result("GetResponse Setup", True, f"Integration ID: {data.get('integration_id')}")
                else:
                    self.log_result("GetResponse Setup", False, f"Setup failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_result("GetResponse Setup", False, f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("GetResponse Setup", False, f"Exception: {str(e)}")
    
    async def test_setup_zapier_integration(self):
        """Test Zapier integration setup"""
        try:
            payload = {
                "affiliate_id": TEST_AFFILIATE_ID,
                "platform": "zapier",
                "api_key": "",  # Zapier uses webhook URL, not API key
                "webhook_url": ZAPIER_WEBHOOK_URL,
                "tags": ["affiliate", "customer"],
                "custom_fields": {"source": "affiliate_program"}
            }
            
            response = await self.client.post(f"{API_BASE}/integrations/setup", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.integration_ids["zapier"] = data.get("integration_id")
                    self.log_result("Zapier Setup", True, f"Integration ID: {data.get('integration_id')}")
                else:
                    self.log_result("Zapier Setup", False, f"Setup failed: {data.get('message', 'Unknown error')}")
            else:
                self.log_result("Zapier Setup", False, f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Zapier Setup", False, f"Exception: {str(e)}")
    
    async def test_get_affiliate_integrations(self):
        """Test getting all integrations for affiliate"""
        try:
            response = await self.client.get(f"{API_BASE}/integrations/{TEST_AFFILIATE_ID}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    integrations = data.get("integrations", [])
                    platforms = [i.get("platform") for i in integrations]
                    expected_platforms = ["convertkit", "getresponse", "zapier"]
                    
                    if all(platform in platforms for platform in expected_platforms):
                        self.log_result("Get Integrations", True, f"Found {len(integrations)} integrations: {platforms}")
                    else:
                        self.log_result("Get Integrations", False, f"Missing platforms. Found: {platforms}")
                else:
                    self.log_result("Get Integrations", False, f"Request failed: {data}")
            else:
                self.log_result("Get Integrations", False, f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Get Integrations", False, f"Exception: {str(e)}")
    
    async def test_integration_connections(self):
        """Test integration connection testing"""
        platforms = ["convertkit", "getresponse", "zapier"]
        
        for platform in platforms:
            try:
                response = await self.client.get(f"{API_BASE}/integrations/test/{TEST_AFFILIATE_ID}/{platform}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        self.log_result(f"Test {platform.title()} Connection", True, f"Connection test passed")
                    else:
                        self.log_result(f"Test {platform.title()} Connection", False, f"Connection test failed: {data.get('test_result', {})}")
                else:
                    self.log_result(f"Test {platform.title()} Connection", False, f"Status {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_result(f"Test {platform.title()} Connection", False, f"Exception: {str(e)}")
    
    async def test_conversion_sync(self):
        """Test conversion syncing to all platforms"""
        try:
            payload = {
                "affiliate_id": TEST_AFFILIATE_ID,
                "customer_email": TEST_CUSTOMER_EMAIL,
                "customer_name": "Test Customer",
                "conversion_value": CONVERSION_VALUE,
                "product_name": "CustomerMind IQ Pro",
                "site_id": "main_site",
                "utm_data": {
                    "utm_source": "affiliate",
                    "utm_medium": "email",
                    "utm_campaign": "test_campaign"
                }
            }
            
            response = await self.client.post(f"{API_BASE}/integrations/sync-conversion", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    synced_platforms = data.get("synced_platforms", [])
                    self.log_result("Conversion Sync", True, f"Synced to {len(synced_platforms)} platforms: {synced_platforms}")
                else:
                    self.log_result("Conversion Sync", False, f"Sync failed: {data}")
            else:
                self.log_result("Conversion Sync", False, f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Conversion Sync", False, f"Exception: {str(e)}")
    
    async def test_webhook_endpoints(self):
        """Test webhook receiver endpoints"""
        platforms = ["convertkit", "getresponse", "zapier"]
        
        for platform in platforms:
            try:
                # Test webhook payload
                test_payload = {
                    "type": "subscriber.subscribe" if platform == "convertkit" else "test_event",
                    "data": {
                        "email": TEST_CUSTOMER_EMAIL,
                        "name": "Test Customer",
                        "timestamp": datetime.now().isoformat()
                    }
                }
                
                response = await self.client.post(
                    f"{API_BASE}/integrations/webhooks/{platform}/{TEST_AFFILIATE_ID}",
                    json=test_payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        self.log_result(f"{platform.title()} Webhook", True, f"Webhook processed successfully")
                    else:
                        self.log_result(f"{platform.title()} Webhook", False, f"Webhook failed: {data}")
                else:
                    self.log_result(f"{platform.title()} Webhook", False, f"Status {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_result(f"{platform.title()} Webhook", False, f"Exception: {str(e)}")
    
    async def test_admin_overview(self):
        """Test admin overview endpoint"""
        try:
            headers = self.get_auth_headers()
            response = await self.client.get(f"{API_BASE}/integrations/admin/overview", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    platform_stats = data.get("platform_stats", [])
                    total_integrations = data.get("total_integrations", 0)
                    self.log_result("Admin Overview", True, f"Found {total_integrations} total integrations across platforms")
                else:
                    self.log_result("Admin Overview", False, f"Request failed: {data}")
            elif response.status_code == 401:
                self.log_result("Admin Overview", False, f"Authentication required - admin token may be invalid")
            else:
                self.log_result("Admin Overview", False, f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Admin Overview", False, f"Exception: {str(e)}")
    
    async def test_admin_logs(self):
        """Test admin webhook logs endpoint"""
        try:
            headers = self.get_auth_headers()
            response = await self.client.get(f"{API_BASE}/integrations/admin/logs", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    logs = data.get("logs", [])
                    self.log_result("Admin Logs", True, f"Retrieved {len(logs)} webhook logs")
                else:
                    self.log_result("Admin Logs", False, f"Request failed: {data}")
            elif response.status_code == 401:
                self.log_result("Admin Logs", False, f"Authentication required - admin token may be invalid")
            else:
                self.log_result("Admin Logs", False, f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Admin Logs", False, f"Exception: {str(e)}")
    
    async def test_delete_integration(self):
        """Test deleting an integration"""
        # Only delete one integration to avoid breaking other tests
        if "zapier" in self.integration_ids:
            try:
                integration_id = self.integration_ids["zapier"]
                response = await self.client.delete(f"{API_BASE}/integrations/{integration_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        self.log_result("Delete Integration", True, f"Successfully deleted Zapier integration")
                    else:
                        self.log_result("Delete Integration", False, f"Delete failed: {data}")
                else:
                    self.log_result("Delete Integration", False, f"Status {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_result("Delete Integration", False, f"Exception: {str(e)}")
        else:
            self.log_result("Delete Integration", False, "No Zapier integration ID available for deletion test")
    
    async def run_all_tests(self):
        """Run all email integration tests"""
        print("🚀 Starting Email Platform Integrations System Testing")
        print("=" * 80)
        
        # Authentication first
        auth_success = await self.authenticate_admin()
        
        # Core system tests
        await self.test_health_check()
        
        # Integration setup tests
        await self.test_setup_convertkit_integration()
        await self.test_setup_getresponse_integration()
        await self.test_setup_zapier_integration()
        
        # Integration management tests
        await self.test_get_affiliate_integrations()
        await self.test_integration_connections()
        
        # Conversion sync test
        await self.test_conversion_sync()
        
        # Webhook tests
        await self.test_webhook_endpoints()
        
        # Admin tests (only if authenticated)
        if auth_success:
            await self.test_admin_overview()
            await self.test_admin_logs()
        
        # Cleanup test
        await self.test_delete_integration()
        
        # Print summary
        await self.print_summary()
    
    async def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("📊 EMAIL PLATFORM INTEGRATIONS TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['details']}")
        
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result["success"]:
                print(f"  • {result['test']}: {result['details']}")
        
        # Overall assessment
        if success_rate >= 80:
            print(f"\n🎉 OVERALL ASSESSMENT: Email Platform Integrations system is PRODUCTION READY")
        elif success_rate >= 60:
            print(f"\n⚠️ OVERALL ASSESSMENT: Email Platform Integrations system needs MINOR FIXES")
        else:
            print(f"\n❌ OVERALL ASSESSMENT: Email Platform Integrations system needs MAJOR FIXES")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

async def main():
    """Main test execution"""
    test_suite = EmailIntegrationsTestSuite()
    try:
        await test_suite.run_all_tests()
    finally:
        await test_suite.close()

if __name__ == "__main__":
    asyncio.run(main())