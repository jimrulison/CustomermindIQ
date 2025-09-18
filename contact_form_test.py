#!/usr/bin/env python3
"""
Contact Form Backend Testing

Test the contact form endpoints found in the ODOO integration module.
"""

import asyncio
import json
import requests
from datetime import datetime
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BACKEND_URL = "https://customeriq-fix.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class ContactFormTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.auth_token = None
        
    def make_request(self, method: str, endpoint: str, data: dict = None, headers: dict = None) -> tuple:
        """Make HTTP request and return response with timing"""
        url = f"{API_BASE}{endpoint}"
        request_headers = {"Content-Type": "application/json"}
        
        if headers:
            request_headers.update(headers)
            
        if self.auth_token:
            request_headers["Authorization"] = f"Bearer {self.auth_token}"
            
        start_time = datetime.now()
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=request_headers, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=request_headers, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response_time = (datetime.now() - start_time).total_seconds()
            return response, response_time
            
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            print(f"Request error: {e}")
            return None, response_time
    
    async def authenticate(self):
        """Authenticate as admin"""
        print("🔐 Authenticating as admin...")
        
        login_data = {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        response, response_time = self.make_request("POST", "/auth/login", login_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if "access_token" in data:
                    self.auth_token = data["access_token"]
                    print(f"✅ Authentication successful ({response_time:.3f}s)")
                    return True
                else:
                    print(f"❌ No access token in response: {data}")
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON response: {response.text[:100]}")
        else:
            error_msg = f"HTTP {response.status_code}" if response else "Connection failed"
            print(f"❌ Authentication failed: {error_msg}")
        
        return False
    
    async def test_contact_form_submission(self):
        """Test contact form submission endpoint"""
        print("\n📧 Testing Contact Form Submission...")
        
        contact_data = {
            "name": "Test User",
            "email": "test@example.com",
            "company": "Test Company",
            "phone": "+1234567890",
            "subject": "Test Contact Form Submission",
            "message": "This is a test message from the backend testing script to verify the contact form functionality is working correctly."
        }
        
        response, response_time = self.make_request("POST", "/odoo/contact-form/submit", contact_data)
        
        if response:
            print(f"Status Code: {response.status_code}")
            print(f"Response Time: {response_time:.3f}s")
            
            try:
                data = response.json()
                print(f"Response Data: {json.dumps(data, indent=2)}")
                
                if response.status_code == 200:
                    print("✅ Contact form submission successful")
                    return True
                else:
                    print(f"❌ Contact form submission failed: {data}")
            except json.JSONDecodeError:
                print(f"Response Text: {response.text[:500]}")
                if response.status_code == 200:
                    print("✅ Contact form submission successful (non-JSON response)")
                    return True
        else:
            print("❌ Contact form submission failed - no response")
        
        return False
    
    async def test_admin_contact_forms(self):
        """Test admin contact forms endpoints"""
        print("\n👑 Testing Admin Contact Forms...")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        # Test getting all contact forms
        response, response_time = self.make_request("GET", "/odoo/admin/contact-forms")
        
        if response:
            print(f"GET /admin/contact-forms - Status: {response.status_code} ({response_time:.3f}s)")
            
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                if response.status_code == 200:
                    print("✅ Admin contact forms endpoint working")
                    return True
                else:
                    print(f"❌ Admin contact forms failed: {data}")
            except json.JSONDecodeError:
                print(f"Response Text: {response.text[:500]}")
        else:
            print("❌ Admin contact forms failed - no response")
        
        return False
    
    async def test_contact_form_stats(self):
        """Test contact form statistics endpoint"""
        print("\n📊 Testing Contact Form Statistics...")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        response, response_time = self.make_request("GET", "/odoo/admin/contact-forms/stats")
        
        if response:
            print(f"GET /admin/contact-forms/stats - Status: {response.status_code} ({response_time:.3f}s)")
            
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                if response.status_code == 200:
                    print("✅ Contact form stats endpoint working")
                    return True
                else:
                    print(f"❌ Contact form stats failed: {data}")
            except json.JSONDecodeError:
                print(f"Response Text: {response.text[:500]}")
        else:
            print("❌ Contact form stats failed - no response")
        
        return False

async def main():
    """Main test execution"""
    print("🚀 Starting Contact Form Backend Testing...")
    print(f"🎯 Target: {BACKEND_URL}")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = ContactFormTester()
    
    # Authenticate first
    auth_success = await tester.authenticate()
    
    # Test contact form endpoints
    results = []
    
    # Test 1: Contact form submission (public endpoint)
    result1 = await tester.test_contact_form_submission()
    results.append(("Contact Form Submission", result1))
    
    if auth_success:
        # Test 2: Admin contact forms
        result2 = await tester.test_admin_contact_forms()
        results.append(("Admin Contact Forms", result2))
        
        # Test 3: Contact form stats
        result3 = await tester.test_contact_form_stats()
        results.append(("Contact Form Stats", result3))
    
    # Summary
    print(f"\n" + "="*60)
    print("📋 CONTACT FORM TESTING SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All contact form tests passed!")
    else:
        print("⚠️ Some contact form tests failed")

if __name__ == "__main__":
    asyncio.run(main())