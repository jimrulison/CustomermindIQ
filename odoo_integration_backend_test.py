#!/usr/bin/env python3
"""
ODOO Integration System Backend Testing
Testing ODOO connection, email integration, customer sync, and integration status
"""

import asyncio
import httpx
import json
import os
from datetime import datetime
from typing import Dict, Any, List

# Test Configuration
BACKEND_URL = "https://global-customer-iq.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class ODOOIntegrationTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.token = None
        self.test_results = []
        
    async def authenticate(self) -> bool:
        """Authenticate with admin credentials"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/auth/login",
                    json={
                        "email": ADMIN_EMAIL,
                        "password": ADMIN_PASSWORD
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get("access_token")
                    print(f"✅ Authentication successful - Token: {self.token[:20]}...")
                    return True
                else:
                    print(f"❌ Authentication failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def test_odoo_connection(self) -> Dict[str, Any]:
        """Test ODOO connection endpoint"""
        print("\n🔗 Testing ODOO Connection...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/connection/test"
                )
                
                result = {
                    "test": "ODOO Connection Test",
                    "endpoint": "/api/odoo/connection/test",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    result["connected"] = data.get("connected", False)
                    result["message"] = data.get("message", "")
                    
                    if data.get("connected"):
                        print(f"✅ ODOO Connection: {data.get('message')}")
                        print(f"   Database: {data.get('database', 'N/A')}")
                        print(f"   User ID: {data.get('user_id', 'N/A')}")
                        print(f"   Version: {data.get('version', 'N/A')}")
                    else:
                        print(f"⚠️ ODOO Connection failed: {data.get('message')}")
                else:
                    result["error"] = response.text
                    print(f"❌ Connection test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "ODOO Connection Test",
                "endpoint": "/api/odoo/connection/test",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Connection test error: {e}")
            return result
    
    async def test_odoo_email_templates(self) -> Dict[str, Any]:
        """Test ODOO email templates endpoint"""
        print("\n📧 Testing ODOO Email Templates...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/email/templates",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "ODOO Email Templates",
                    "endpoint": "/api/odoo/email/templates",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    templates = data.get("templates", [])
                    result["template_count"] = len(templates)
                    
                    print(f"✅ Email Templates Retrieved: {len(templates)} templates found")
                    if templates:
                        print("   Template Names:")
                        for template in templates[:5]:  # Show first 5
                            print(f"   - {template.get('name', 'Unnamed')}")
                    else:
                        print("   No templates found in ODOO")
                else:
                    result["error"] = response.text
                    print(f"❌ Email templates test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "ODOO Email Templates",
                "endpoint": "/api/odoo/email/templates",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Email templates test error: {e}")
            return result
    
    async def test_create_default_templates(self) -> Dict[str, Any]:
        """Test creating default Customer Mind IQ templates"""
        print("\n🎨 Testing Create Default Templates...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/odoo/email/templates/create-defaults",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "Create Default Email Templates",
                    "endpoint": "/api/odoo/email/templates/create-defaults",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    created_count = data.get("created_count", 0)
                    result["created_count"] = created_count
                    
                    print(f"✅ Default Templates Created: {created_count} templates")
                    templates = data.get("templates", [])
                    if templates:
                        print("   Created Templates:")
                        for template in templates:
                            print(f"   - {template.get('name')} (ID: {template.get('template_id')})")
                else:
                    result["error"] = response.text
                    print(f"❌ Create default templates failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Create Default Email Templates",
                "endpoint": "/api/odoo/email/templates/create-defaults",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Create default templates error: {e}")
            return result
    
    async def test_integration_status(self) -> Dict[str, Any]:
        """Test ODOO integration status endpoint"""
        print("\n📊 Testing ODOO Integration Status...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/integration/status",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "ODOO Integration Status",
                    "endpoint": "/api/odoo/integration/status",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    
                    connection = data.get("connection", {})
                    statistics = data.get("statistics", {})
                    features = data.get("features", {})
                    
                    print(f"✅ Integration Status Retrieved")
                    print(f"   Connection Status: {connection.get('status', 'unknown')}")
                    print(f"   Connected: {connection.get('connected', False)}")
                    print(f"   Email Templates: {statistics.get('email_templates', 0)}")
                    print(f"   Customers Available: {statistics.get('customers_available', 0)}")
                    print(f"   Campaigns (30 days): {statistics.get('campaigns_last_30_days', 0)}")
                    print(f"   Features Available: {list(features.keys())}")
                else:
                    result["error"] = response.text
                    print(f"❌ Integration status test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "ODOO Integration Status",
                "endpoint": "/api/odoo/integration/status",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Integration status test error: {e}")
            return result
    
    async def test_email_providers_current(self) -> Dict[str, Any]:
        """Test email providers current endpoint"""
        print("\n📮 Testing Email Providers Current...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/email/email/providers/current",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "Email Providers Current",
                    "endpoint": "/api/email/email/providers/current",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    
                    provider = data.get("provider", {})
                    print(f"✅ Current Email Provider Retrieved")
                    print(f"   Provider: {provider.get('name', 'Unknown')}")
                    print(f"   Type: {provider.get('type', 'Unknown')}")
                    print(f"   Status: {provider.get('status', 'Unknown')}")
                    print(f"   ODOO Integration: {provider.get('odoo_integration', False)}")
                else:
                    result["error"] = response.text
                    print(f"❌ Email providers test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Email Providers Current",
                "endpoint": "/api/email/email/providers/current",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Email providers test error: {e}")
            return result
    
    async def test_customer_sync(self) -> Dict[str, Any]:
        """Test ODOO customer sync endpoint"""
        print("\n👥 Testing ODOO Customer Sync...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/customers/sync",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "ODOO Customer Sync",
                    "endpoint": "/api/odoo/customers/sync",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    
                    synced_count = data.get("synced_count", 0)
                    result["synced_count"] = synced_count
                    
                    print(f"✅ Customer Sync Completed")
                    print(f"   Status: {data.get('status', 'unknown')}")
                    print(f"   Synced Count: {synced_count}")
                    print(f"   Message: {data.get('message', 'No message')}")
                    
                    if synced_count == 0:
                        print("   ⚠️ No customers found in ODOO or sync failed")
                else:
                    result["error"] = response.text
                    print(f"❌ Customer sync test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "ODOO Customer Sync",
                "endpoint": "/api/odoo/customers/sync",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Customer sync test error: {e}")
            return result
    
    async def test_contact_form_submission(self) -> Dict[str, Any]:
        """Test contact form submission (public endpoint)"""
        print("\n📝 Testing Contact Form Submission...")
        
        try:
            # Test data for contact form
            contact_data = {
                "name": "Test Customer",
                "email": "test@example.com",
                "phone": "+1-555-0123",
                "company": "Test Company Inc",
                "subject": "ODOO Integration Testing",
                "message": "This is a test message for ODOO integration testing. Please verify that this contact form submission is properly processed and integrated with ODOO CRM system.",
                "website": "https://testcompany.com",
                "source": "website_contact_form"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/odoo/contact-form/submit",
                    json=contact_data
                )
                
                result = {
                    "test": "Contact Form Submission",
                    "endpoint": "/api/odoo/contact-form/submit",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    
                    form_id = data.get("form_id")
                    result["form_id"] = form_id
                    
                    print(f"✅ Contact Form Submitted Successfully")
                    print(f"   Status: {data.get('status', 'unknown')}")
                    print(f"   Form ID: {form_id}")
                    print(f"   Reference: {data.get('reference', 'N/A')}")
                    print(f"   Message: {data.get('message', 'No message')}")
                else:
                    result["error"] = response.text
                    print(f"❌ Contact form submission failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Contact Form Submission",
                "endpoint": "/api/odoo/contact-form/submit",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Contact form submission error: {e}")
            return result
    
    async def run_all_tests(self):
        """Run all ODOO integration tests"""
        print("🚀 Starting ODOO Integration System Backend Testing")
        print("=" * 60)
        
        # Authenticate first
        if not await self.authenticate():
            print("❌ Authentication failed - cannot proceed with tests")
            return
        
        # Run all tests
        tests = [
            self.test_odoo_connection(),
            self.test_odoo_email_templates(),
            self.test_create_default_templates(),
            self.test_integration_status(),
            self.test_email_providers_current(),
            self.test_customer_sync(),
            self.test_contact_form_submission()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Process results
        successful_tests = 0
        total_tests = len(results)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.test_results.append({
                    "test": f"Test {i+1}",
                    "success": False,
                    "error": str(result)
                })
            else:
                self.test_results.append(result)
                if result.get("success", False):
                    successful_tests += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 ODOO Integration Testing Summary")
        print("=" * 60)
        
        success_rate = (successful_tests / total_tests) * 100
        print(f"✅ Tests Passed: {successful_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if successful_tests == total_tests:
            print("🎉 All ODOO integration tests passed!")
        elif successful_tests > total_tests * 0.7:
            print("⚠️ Most tests passed - minor issues detected")
        else:
            print("❌ Multiple test failures - requires investigation")
        
        # Detailed results
        print("\n📋 Detailed Test Results:")
        for i, result in enumerate(self.test_results, 1):
            status = "✅ PASS" if result.get("success") else "❌ FAIL"
            test_name = result.get("test", f"Test {i}")
            print(f"{i}. {status} - {test_name}")
            
            if not result.get("success") and result.get("error"):
                print(f"   Error: {result['error']}")
        
        # Key findings
        print("\n🔍 Key Findings:")
        
        # Connection status
        connection_test = next((r for r in self.test_results if "Connection" in r.get("test", "")), None)
        if connection_test and connection_test.get("success"):
            if connection_test.get("connected"):
                print("✅ ODOO connection is working properly")
            else:
                print("⚠️ ODOO connection test passed but connection failed")
        else:
            print("❌ ODOO connection test failed")
        
        # Email integration
        email_tests = [r for r in self.test_results if "Email" in r.get("test", "")]
        email_success = sum(1 for r in email_tests if r.get("success"))
        if email_success == len(email_tests) and email_tests:
            print("✅ Email integration is fully functional")
        elif email_success > 0:
            print("⚠️ Email integration partially working")
        else:
            print("❌ Email integration has issues")
        
        # Customer sync
        sync_test = next((r for r in self.test_results if "Sync" in r.get("test", "")), None)
        if sync_test and sync_test.get("success"):
            synced_count = sync_test.get("synced_count", 0)
            if synced_count > 0:
                print(f"✅ Customer sync working - {synced_count} customers synced")
            else:
                print("⚠️ Customer sync working but no customers found")
        else:
            print("❌ Customer sync has issues")
        
        # Contact form
        form_test = next((r for r in self.test_results if "Contact" in r.get("test", "")), None)
        if form_test and form_test.get("success"):
            print("✅ Contact form integration working")
        else:
            print("❌ Contact form integration has issues")
        
        print("\n" + "=" * 60)
        print("🏁 ODOO Integration Testing Complete")
        print("=" * 60)

async def main():
    """Main test execution"""
    tester = ODOOIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())