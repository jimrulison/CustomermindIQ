#!/usr/bin/env python3
"""
Email Platform Integrations Admin Endpoints Authorization Test
Testing admin authentication, authorization, and integration functionality
"""

import asyncio
import httpx
import json
import os
from datetime import datetime
from typing import Dict, Any

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customeriq-hub.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials from review request
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class EmailIntegrationsAdminTester:
    def __init__(self):
        self.session = httpx.AsyncClient(timeout=30.0)
        self.admin_token = None
        self.test_results = []
        self.integration_id = None
        
    async def log_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        if response_data:
            result["response_size"] = len(str(response_data))
        self.test_results.append(result)
        print(f"{status} {test_name}: {details}")
        
    async def admin_login(self) -> bool:
        """Test admin authentication"""
        try:
            response = await self.session.post(f"{API_BASE}/auth/login", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                user_profile = data.get("user_profile", {})
                await self.log_result(
                    "Admin Authentication", 
                    True, 
                    f"Admin login successful, role: {user_profile.get('role')}, tier: {user_profile.get('subscription_tier')}, token length: {len(self.admin_token) if self.admin_token else 0}"
                )
                return True
            else:
                await self.log_result(
                    "Admin Authentication", 
                    False, 
                    f"Login failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Admin Authentication", False, f"Login error: {str(e)}")
            return False
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        if not self.admin_token:
            return {}
        return {"Authorization": f"Bearer {self.admin_token}"}
    
    async def test_admin_integrations_overview(self):
        """Test /api/integrations/admin/overview endpoint"""
        try:
            response = await self.session.get(
                f"{API_BASE}/integrations/admin/overview",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                await self.log_result(
                    "Admin Integrations Overview", 
                    True, 
                    f"Overview retrieved successfully, platform stats: {len(data.get('platform_stats', []))}, total integrations: {data.get('total_integrations', 0)}",
                    data
                )
                return True
            else:
                await self.log_result(
                    "Admin Integrations Overview", 
                    False, 
                    f"Failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Admin Integrations Overview", False, f"Error: {str(e)}")
            return False
    
    async def test_admin_integrations_logs(self):
        """Test /api/integrations/admin/logs endpoint"""
        try:
            response = await self.session.get(
                f"{API_BASE}/integrations/admin/logs",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                await self.log_result(
                    "Admin Integration Logs", 
                    True, 
                    f"Logs retrieved successfully, total logs: {data.get('total', 0)}",
                    data
                )
                return True
            else:
                await self.log_result(
                    "Admin Integration Logs", 
                    False, 
                    f"Failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Admin Integration Logs", False, f"Error: {str(e)}")
            return False
    
    async def test_unauthorized_access(self):
        """Test unauthorized access to admin endpoints"""
        try:
            # Test without token
            response = await self.session.get(f"{API_BASE}/integrations/admin/overview")
            
            if response.status_code in [401, 403]:
                await self.log_result(
                    "Unauthorized Access Protection", 
                    True, 
                    f"Correctly blocked unauthorized access with status {response.status_code}"
                )
                return True
            else:
                await self.log_result(
                    "Unauthorized Access Protection", 
                    False, 
                    f"Should have returned 401/403 but got {response.status_code}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Unauthorized Access Protection", False, f"Error: {str(e)}")
            return False
    
    async def test_setup_convertkit_integration(self):
        """Test setting up a ConvertKit integration"""
        try:
            test_data = {
                "affiliate_id": "test_admin_affiliate",
                "platform": "convertkit",
                "api_key": "test_api_key_12345",
                "webhook_url": "https://example.com/webhook",
                "tags": ["affiliate", "customer", "test"],
                "custom_fields": {
                    "source": "admin_test",
                    "test_field": "test_value"
                }
            }
            
            response = await self.session.post(
                f"{API_BASE}/integrations/setup",
                json=test_data,
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                self.integration_id = data.get("integration_id")
                await self.log_result(
                    "ConvertKit Integration Setup", 
                    True, 
                    f"Integration created successfully, ID: {self.integration_id}, status: {data.get('status')}",
                    data
                )
                return True
            else:
                await self.log_result(
                    "ConvertKit Integration Setup", 
                    False, 
                    f"Setup failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            await self.log_result("ConvertKit Integration Setup", False, f"Error: {str(e)}")
            return False
    
    async def test_get_affiliate_integrations(self):
        """Test getting integrations for an affiliate"""
        try:
            response = await self.session.get(
                f"{API_BASE}/integrations/test_admin_affiliate",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                await self.log_result(
                    "Get Affiliate Integrations", 
                    True, 
                    f"Retrieved {data.get('total', 0)} integrations for affiliate",
                    data
                )
                return True
            else:
                await self.log_result(
                    "Get Affiliate Integrations", 
                    False, 
                    f"Failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Get Affiliate Integrations", False, f"Error: {str(e)}")
            return False
    
    async def test_integration_testing(self):
        """Test the integration testing functionality"""
        try:
            response = await self.session.get(
                f"{API_BASE}/integrations/test/test_admin_affiliate/convertkit",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                await self.log_result(
                    "Integration Testing", 
                    True, 
                    f"Integration test completed, success: {data.get('success')}, status: {data.get('status')}",
                    data
                )
                return True
            else:
                await self.log_result(
                    "Integration Testing", 
                    False, 
                    f"Test failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Integration Testing", False, f"Error: {str(e)}")
            return False
    
    async def test_sync_conversion(self):
        """Test conversion sync functionality"""
        try:
            conversion_data = {
                "affiliate_id": "test_admin_affiliate",
                "customer_email": "test.customer@example.com",
                "customer_name": "Test Customer",
                "conversion_value": 99.99,
                "product_name": "Test Product",
                "site_id": "main_site",
                "utm_data": {
                    "utm_source": "admin_test",
                    "utm_medium": "email",
                    "utm_campaign": "test_campaign"
                }
            }
            
            response = await self.session.post(
                f"{API_BASE}/integrations/sync-conversion",
                json=conversion_data,
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                await self.log_result(
                    "Conversion Sync", 
                    True, 
                    f"Conversion sync initiated, platforms: {len(data.get('synced_platforms', []))}, total integrations: {data.get('total_integrations', 0)}",
                    data
                )
                return True
            else:
                await self.log_result(
                    "Conversion Sync", 
                    False, 
                    f"Sync failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Conversion Sync", False, f"Error: {str(e)}")
            return False
    
    async def test_integration_health(self):
        """Test integration system health check"""
        try:
            response = await self.session.get(f"{API_BASE}/integrations/health")
            
            if response.status_code == 200:
                data = response.json()
                await self.log_result(
                    "Integration Health Check", 
                    True, 
                    f"Health check passed, status: {data.get('status')}, platforms supported: {len(data.get('platforms_supported', []))}",
                    data
                )
                return True
            else:
                await self.log_result(
                    "Integration Health Check", 
                    False, 
                    f"Health check failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Integration Health Check", False, f"Error: {str(e)}")
            return False
    
    async def test_invalid_data_handling(self):
        """Test handling of invalid data"""
        try:
            # Test with invalid platform
            invalid_data = {
                "affiliate_id": "test_affiliate",
                "platform": "invalid_platform",
                "api_key": "test_key"
            }
            
            response = await self.session.post(
                f"{API_BASE}/integrations/setup",
                json=invalid_data,
                headers=self.get_auth_headers()
            )
            
            if response.status_code in [400, 422]:
                await self.log_result(
                    "Invalid Data Handling", 
                    True, 
                    f"Correctly rejected invalid data with status {response.status_code}"
                )
                return True
            else:
                await self.log_result(
                    "Invalid Data Handling", 
                    False, 
                    f"Should have rejected invalid data but got status {response.status_code}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Invalid Data Handling", False, f"Error: {str(e)}")
            return False
    
    async def test_delete_integration(self):
        """Test deleting an integration"""
        try:
            if not self.integration_id:
                await self.log_result(
                    "Delete Integration", 
                    False, 
                    "No integration ID available for deletion test"
                )
                return False
            
            response = await self.session.delete(
                f"{API_BASE}/integrations/{self.integration_id}",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                await self.log_result(
                    "Delete Integration", 
                    True, 
                    f"Integration deleted successfully: {data.get('message')}",
                    data
                )
                return True
            else:
                await self.log_result(
                    "Delete Integration", 
                    False, 
                    f"Delete failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            await self.log_result("Delete Integration", False, f"Error: {str(e)}")
            return False
    
    async def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🚀 Starting Email Platform Integrations Admin Endpoints Testing")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Testing with admin credentials: {ADMIN_EMAIL}")
        print("=" * 80)
        
        # Step 1: Admin Authentication
        if not await self.admin_login():
            print("❌ Admin authentication failed - cannot proceed with tests")
            return
        
        # Step 2: Test unauthorized access protection
        await self.test_unauthorized_access()
        
        # Step 3: Test admin endpoints with proper authentication
        await self.test_admin_integrations_overview()
        await self.test_admin_integrations_logs()
        
        # Step 4: Test integration system health
        await self.test_integration_health()
        
        # Step 5: Test integration setup and management
        await self.test_setup_convertkit_integration()
        await self.test_get_affiliate_integrations()
        await self.test_integration_testing()
        
        # Step 6: Test conversion sync functionality
        await self.test_sync_conversion()
        
        # Step 7: Test error handling
        await self.test_invalid_data_handling()
        
        # Step 8: Test integration deletion
        await self.test_delete_integration()
        
        # Generate summary
        await self.generate_summary()
    
    async def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 80)
        print("📊 EMAIL PLATFORM INTEGRATIONS ADMIN TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        # Show failed tests
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['details']}")
            print()
        
        # Show passed tests
        print("✅ PASSED TESTS:")
        for result in self.test_results:
            if result["success"]:
                print(f"  • {result['test']}: {result['details']}")
        
        print("\n" + "=" * 80)
        
        # Overall assessment
        if success_rate >= 90:
            print("🎉 EXCELLENT: Email Platform Integrations admin system is working correctly!")
        elif success_rate >= 75:
            print("✅ GOOD: Most admin functionality is working with minor issues")
        elif success_rate >= 50:
            print("⚠️ MODERATE: Admin system has significant issues that need attention")
        else:
            print("❌ CRITICAL: Admin system has major problems requiring immediate fixes")
        
        print("=" * 80)
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.session.aclose()

async def main():
    """Main test execution"""
    tester = EmailIntegrationsAdminTester()
    try:
        await tester.run_comprehensive_test()
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    asyncio.run(main())