#!/usr/bin/env python3
"""
Admin Manual Download Endpoint Testing
=====================================

This test specifically focuses on testing the admin manual download endpoint
as requested in the review:

1. Admin Authentication - Login with admin@customermindiq.com / CustomerMindIQ2025!
2. Admin Manual Download Endpoint - Test GET /api/download/admin-training-manual 
3. HEAD Request Support - Test HEAD /api/download/admin-training-manual

The user has been complaining that the admin manual download is broken despite 
multiple previous "fixes". This test will verify if the endpoint is actually 
working correctly.
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime

# Configuration
BACKEND_URL = "https://admin-portal-fix-9.preview.emergentagent.com"
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class AdminManualDownloadTester:
    def __init__(self):
        self.session = None
        self.auth_token = None
        self.test_results = []
        
    async def setup_session(self):
        """Setup HTTP session with proper headers"""
        connector = aiohttp.TCPConnector(ssl=False)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'AdminManualDownloadTester/1.0',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
        )
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            
    def log_result(self, test_name, success, details, response_time=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "response_time": f"{response_time:.3f}s" if response_time else "N/A",
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} {test_name}: {details}")
        if response_time:
            print(f"    Response Time: {response_time:.3f}s")
        print()
        
    async def test_admin_authentication(self):
        """Test 1: Admin Authentication"""
        print("🔐 Testing Admin Authentication...")
        
        try:
            start_time = asyncio.get_event_loop().time()
            
            login_data = {
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            }
            
            async with self.session.post(
                f"{BACKEND_URL}/api/auth/login",
                json=login_data,
                headers={'Content-Type': 'application/json'}
            ) as response:
                response_time = asyncio.get_event_loop().time() - start_time
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        data = json.loads(response_text)
                        if 'access_token' in data:
                            self.auth_token = data['access_token']
                            self.log_result(
                                "Admin Authentication",
                                True,
                                f"Successfully authenticated admin user. Token received (length: {len(self.auth_token)})",
                                response_time
                            )
                            return True
                        else:
                            self.log_result(
                                "Admin Authentication",
                                False,
                                f"Login successful but no access_token in response: {response_text[:200]}",
                                response_time
                            )
                            return False
                    except json.JSONDecodeError:
                        self.log_result(
                            "Admin Authentication",
                            False,
                            f"Invalid JSON response: {response_text[:200]}",
                            response_time
                        )
                        return False
                else:
                    self.log_result(
                        "Admin Authentication",
                        False,
                        f"Login failed with status {response.status}: {response_text[:200]}",
                        response_time
                    )
                    return False
                    
        except Exception as e:
            self.log_result(
                "Admin Authentication",
                False,
                f"Authentication error: {str(e)}"
            )
            return False
            
    async def test_admin_manual_download_get(self):
        """Test 2: Admin Manual Download - GET Request"""
        print("📥 Testing Admin Manual Download (GET)...")
        
        if not self.auth_token:
            self.log_result(
                "Admin Manual Download (GET)",
                False,
                "Cannot test - no authentication token available"
            )
            return False
            
        try:
            start_time = asyncio.get_event_loop().time()
            
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            async with self.session.get(
                f"{BACKEND_URL}/api/download/admin-training-manual",
                headers=headers
            ) as response:
                response_time = asyncio.get_event_loop().time() - start_time
                
                if response.status == 200:
                    # Check response headers
                    content_type = response.headers.get('content-type', '')
                    content_disposition = response.headers.get('content-disposition', '')
                    content_length = response.headers.get('content-length', 'unknown')
                    
                    # Read response content
                    content = await response.text()
                    content_size = len(content)
                    
                    # Check if content contains expected admin manual content
                    contains_admin_manual = "CustomerMind IQ - Admin Training Manual" in content
                    contains_html = content.strip().startswith('<!DOCTYPE html') or content.strip().startswith('<html')
                    
                    success = (
                        content_type.startswith('text/html') and
                        'attachment' in content_disposition and
                        contains_admin_manual and
                        contains_html and
                        content_size > 1000  # Should be substantial content
                    )
                    
                    details = f"Status: {response.status}, Content-Type: {content_type}, " \
                             f"Content-Disposition: {content_disposition}, Size: {content_size} chars, " \
                             f"Contains Admin Manual Title: {contains_admin_manual}, " \
                             f"Valid HTML: {contains_html}"
                    
                    self.log_result(
                        "Admin Manual Download (GET)",
                        success,
                        details,
                        response_time
                    )
                    
                    if success:
                        print(f"    ✅ File download headers correct")
                        print(f"    ✅ Content contains admin manual title")
                        print(f"    ✅ Content is valid HTML ({content_size:,} characters)")
                        print(f"    ✅ Content-Disposition indicates file attachment")
                    
                    return success
                    
                else:
                    response_text = await response.text()
                    self.log_result(
                        "Admin Manual Download (GET)",
                        False,
                        f"HTTP {response.status}: {response_text[:200]}",
                        response_time
                    )
                    return False
                    
        except Exception as e:
            self.log_result(
                "Admin Manual Download (GET)",
                False,
                f"Download error: {str(e)}"
            )
            return False
            
    async def test_admin_manual_download_head(self):
        """Test 3: Admin Manual Download - HEAD Request (Preflight Check)"""
        print("🔍 Testing Admin Manual Download (HEAD)...")
        
        if not self.auth_token:
            self.log_result(
                "Admin Manual Download (HEAD)",
                False,
                "Cannot test - no authentication token available"
            )
            return False
            
        try:
            start_time = asyncio.get_event_loop().time()
            
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            async with self.session.head(
                f"{BACKEND_URL}/api/download/admin-training-manual",
                headers=headers
            ) as response:
                response_time = asyncio.get_event_loop().time() - start_time
                
                if response.status == 200:
                    # Check response headers (HEAD should return same headers as GET but no body)
                    content_type = response.headers.get('content-type', '')
                    content_disposition = response.headers.get('content-disposition', '')
                    content_length = response.headers.get('content-length', 'unknown')
                    
                    # HEAD request should not have body content
                    content = await response.text()
                    has_no_body = len(content) == 0
                    
                    success = (
                        content_type.startswith('text/html') and
                        'attachment' in content_disposition and
                        has_no_body  # HEAD should not return body
                    )
                    
                    details = f"Status: {response.status}, Content-Type: {content_type}, " \
                             f"Content-Disposition: {content_disposition}, " \
                             f"Content-Length: {content_length}, No Body: {has_no_body}"
                    
                    self.log_result(
                        "Admin Manual Download (HEAD)",
                        success,
                        details,
                        response_time
                    )
                    
                    if success:
                        print(f"    ✅ HEAD request returns proper headers")
                        print(f"    ✅ No response body (as expected for HEAD)")
                        print(f"    ✅ Content-Disposition indicates file attachment")
                    
                    return success
                    
                else:
                    response_text = await response.text()
                    self.log_result(
                        "Admin Manual Download (HEAD)",
                        False,
                        f"HTTP {response.status}: {response_text[:200]}",
                        response_time
                    )
                    return False
                    
        except Exception as e:
            self.log_result(
                "Admin Manual Download (HEAD)",
                False,
                f"HEAD request error: {str(e)}"
            )
            return False
            
    async def test_file_existence_check(self):
        """Test 4: Verify Admin Manual File Exists on Server"""
        print("📁 Testing Admin Manual File Existence...")
        
        try:
            # Check if the file exists locally (since we're running on the same server)
            file_path = "/app/CustomerMind_IQ_Admin_Training_Manual_Professional.html"
            
            if os.path.exists(file_path):
                # Get file size and check content
                file_size = os.path.getsize(file_path)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)  # Read first 1000 chars
                    contains_title = "CustomerMind IQ - Admin Training Manual" in content
                    is_html = content.strip().startswith('<!DOCTYPE html') or content.strip().startswith('<html')
                
                success = file_size > 1000 and contains_title and is_html
                
                details = f"File exists at {file_path}, Size: {file_size:,} bytes, " \
                         f"Contains title: {contains_title}, Valid HTML: {is_html}"
                
                self.log_result(
                    "Admin Manual File Existence",
                    success,
                    details
                )
                
                if success:
                    print(f"    ✅ File exists and is accessible")
                    print(f"    ✅ File size is substantial ({file_size:,} bytes)")
                    print(f"    ✅ File contains expected admin manual title")
                    print(f"    ✅ File is valid HTML format")
                
                return success
            else:
                self.log_result(
                    "Admin Manual File Existence",
                    False,
                    f"File not found at expected path: {file_path}"
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Admin Manual File Existence",
                False,
                f"File check error: {str(e)}"
            )
            return False
            
    async def test_unauthenticated_access(self):
        """Test 5: Verify Endpoint Requires Authentication"""
        print("🚫 Testing Unauthenticated Access (Should Fail)...")
        
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Try to access without authentication
            async with self.session.get(
                f"{BACKEND_URL}/api/download/admin-training-manual"
            ) as response:
                response_time = asyncio.get_event_loop().time() - start_time
                
                # Should return 401 or 403 for unauthenticated access
                success = response.status in [401, 403]
                
                response_text = await response.text()
                
                details = f"Status: {response.status} (Expected 401/403), Response: {response_text[:100]}"
                
                self.log_result(
                    "Unauthenticated Access Protection",
                    success,
                    details,
                    response_time
                )
                
                if success:
                    print(f"    ✅ Endpoint properly protected from unauthenticated access")
                else:
                    print(f"    ⚠️  Endpoint may not be properly protected (returned {response.status})")
                
                return success
                
        except Exception as e:
            self.log_result(
                "Unauthenticated Access Protection",
                False,
                f"Test error: {str(e)}"
            )
            return False
            
    async def run_all_tests(self):
        """Run all admin manual download tests"""
        print("🎯 ADMIN MANUAL DOWNLOAD ENDPOINT TESTING")
        print("=" * 60)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Admin Email: {ADMIN_EMAIL}")
        print(f"Test Time: {datetime.now().isoformat()}")
        print()
        
        await self.setup_session()
        
        try:
            # Test sequence
            tests = [
                ("File Existence Check", self.test_file_existence_check),
                ("Admin Authentication", self.test_admin_authentication),
                ("Admin Manual Download (GET)", self.test_admin_manual_download_get),
                ("Admin Manual Download (HEAD)", self.test_admin_manual_download_head),
                ("Unauthenticated Access Protection", self.test_unauthenticated_access)
            ]
            
            passed_tests = 0
            total_tests = len(tests)
            
            for test_name, test_func in tests:
                try:
                    result = await test_func()
                    if result:
                        passed_tests += 1
                except Exception as e:
                    print(f"❌ {test_name} failed with exception: {e}")
                    self.log_result(test_name, False, f"Exception: {str(e)}")
            
            # Summary
            print("=" * 60)
            print("🎯 ADMIN MANUAL DOWNLOAD TEST SUMMARY")
            print("=" * 60)
            
            success_rate = (passed_tests / total_tests) * 100
            print(f"Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
            print()
            
            for result in self.test_results:
                print(f"{result['status']} {result['test']}")
                print(f"    {result['details']}")
                if result['response_time'] != "N/A":
                    print(f"    Response Time: {result['response_time']}")
                print()
            
            # Critical Issues Analysis
            critical_issues = []
            if not any(r['success'] and r['test'] == 'Admin Authentication' for r in self.test_results):
                critical_issues.append("❌ CRITICAL: Admin authentication is failing")
            
            if not any(r['success'] and r['test'] == 'Admin Manual Download (GET)' for r in self.test_results):
                critical_issues.append("❌ CRITICAL: Admin manual download (GET) is not working")
                
            if not any(r['success'] and r['test'] == 'Admin Manual File Existence' for r in self.test_results):
                critical_issues.append("❌ CRITICAL: Admin manual file is missing or corrupted")
            
            if critical_issues:
                print("🚨 CRITICAL ISSUES FOUND:")
                for issue in critical_issues:
                    print(f"  {issue}")
                print()
                print("🔧 RECOMMENDED ACTIONS:")
                print("  1. Verify admin credentials are correct")
                print("  2. Check if admin manual file exists and is readable")
                print("  3. Verify endpoint routing and authentication middleware")
                print("  4. Check server logs for detailed error information")
            else:
                print("✅ ALL CRITICAL TESTS PASSED - Admin manual download is working correctly!")
            
            return success_rate >= 80  # Consider successful if 80% or more tests pass
            
        finally:
            await self.cleanup_session()

async def main():
    """Main test execution"""
    tester = AdminManualDownloadTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🎉 ADMIN MANUAL DOWNLOAD TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n💥 ADMIN MANUAL DOWNLOAD TESTING FAILED - ISSUES FOUND")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())