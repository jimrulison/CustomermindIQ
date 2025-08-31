#!/usr/bin/env python3
"""
Authentication Domain Testing for CustomerMind IQ
Testing recent fixes for custom domain connectivity and case-insensitive login functionality
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import sys

# Backend URL from frontend configuration
BACKEND_URL = "https://customermindiq.com"

class AuthenticationTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.session = None
        self.jwt_token = None
        self.test_results = []
        
    async def setup_session(self):
        """Setup HTTP session with proper headers"""
        connector = aiohttp.TCPConnector(ssl=False)  # For testing
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'CustomerMindIQ-Backend-Tester/1.0'
            }
        )
    
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name, success, details, response_time=None):
        """Log test result"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat(),
            'response_time': response_time
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    Details: {details}")
        if response_time:
            print(f"    Response Time: {response_time:.2f}s")
        print()
    
    async def test_health_endpoint(self):
        """Test /api/health endpoint to verify server connectivity"""
        test_name = "Health Check - Server Connectivity"
        try:
            start_time = datetime.now()
            
            async with self.session.get(f"{self.backend_url}/api/health") as response:
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'healthy':
                        self.log_test(test_name, True, 
                                    f"Server healthy, service: {data.get('service', 'Unknown')}", 
                                    response_time)
                        return True
                    else:
                        self.log_test(test_name, False, 
                                    f"Unexpected health status: {data.get('status')}", 
                                    response_time)
                        return False
                else:
                    self.log_test(test_name, False, 
                                f"HTTP {response.status}: {await response.text()}", 
                                response_time)
                    return False
                    
        except Exception as e:
            self.log_test(test_name, False, f"Connection error: {str(e)}")
            return False
    
    async def test_admin_login(self, email, password, test_description):
        """Test admin login with given credentials"""
        test_name = f"Admin Login - {test_description}"
        try:
            start_time = datetime.now()
            
            login_data = {
                "email": email,
                "password": password
            }
            
            async with self.session.post(
                f"{self.backend_url}/api/auth/login", 
                json=login_data
            ) as response:
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                
                if response.status == 200:
                    data = await response.json()
                    if 'access_token' in data:
                        self.jwt_token = data['access_token']
                        user_info = data.get('user', {})
                        self.log_test(test_name, True, 
                                    f"Login successful, role: {user_info.get('role', 'Unknown')}, "
                                    f"email: {user_info.get('email', 'Unknown')}", 
                                    response_time)
                        return True
                    else:
                        self.log_test(test_name, False, 
                                    f"No access token in response: {data}", 
                                    response_time)
                        return False
                else:
                    error_text = await response.text()
                    self.log_test(test_name, False, 
                                f"HTTP {response.status}: {error_text}", 
                                response_time)
                    return False
                    
        except Exception as e:
            self.log_test(test_name, False, f"Login error: {str(e)}")
            return False
    
    async def test_profile_endpoint(self):
        """Test /api/auth/profile endpoint with JWT token"""
        test_name = "Profile Access with JWT Token"
        
        if not self.jwt_token:
            self.log_test(test_name, False, "No JWT token available from login")
            return False
            
        try:
            start_time = datetime.now()
            
            headers = {
                'Authorization': f'Bearer {self.jwt_token}',
                'Content-Type': 'application/json'
            }
            
            async with self.session.get(
                f"{self.backend_url}/api/auth/profile",
                headers=headers
            ) as response:
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                
                if response.status == 200:
                    data = await response.json()
                    user_info = data.get('user', {})
                    self.log_test(test_name, True, 
                                f"Profile retrieved successfully, "
                                f"email: {user_info.get('email', 'Unknown')}, "
                                f"role: {user_info.get('role', 'Unknown')}", 
                                response_time)
                    return True
                else:
                    error_text = await response.text()
                    self.log_test(test_name, False, 
                                f"HTTP {response.status}: {error_text}", 
                                response_time)
                    return False
                    
        except Exception as e:
            self.log_test(test_name, False, f"Profile access error: {str(e)}")
            return False
    
    async def run_authentication_tests(self):
        """Run comprehensive authentication tests"""
        print("🔐 CustomerMind IQ Authentication System Testing")
        print("=" * 60)
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Started: {datetime.now().isoformat()}")
        print()
        
        await self.setup_session()
        
        try:
            # Test 1: Health Check
            health_ok = await self.test_health_endpoint()
            
            if not health_ok:
                print("❌ CRITICAL: Server health check failed. Cannot proceed with authentication tests.")
                return
            
            # Test 2: Admin Login with exact credentials
            admin_login_ok = await self.test_admin_login(
                "admin@customermindiq.com", 
                "CustomerMindIQ2025!",
                "Exact Case Email"
            )
            
            # Test 3: Case-insensitive login (different case)
            case_insensitive_ok = await self.test_admin_login(
                "Admin@CustomermindIQ.com", 
                "CustomerMindIQ2025!",
                "Mixed Case Email (Case-Insensitive Test)"
            )
            
            # Test 4: Profile endpoint with JWT token (if we have one)
            if self.jwt_token:
                await self.test_profile_endpoint()
            
            # Test 5: Another case variation to thoroughly test case-insensitivity
            await self.test_admin_login(
                "ADMIN@CUSTOMERMINDIQ.COM", 
                "CustomerMindIQ2025!",
                "All Uppercase Email (Case-Insensitive Test)"
            )
            
        finally:
            await self.cleanup_session()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("=" * 60)
        print("🔍 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['success']])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        # Detailed results
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}")
            if result['details']:
                print(f"    {result['details']}")
        
        print()
        print("🎯 KEY FINDINGS:")
        
        # Check specific requirements from review request
        health_tests = [r for r in self.test_results if 'Health Check' in r['test']]
        exact_login_tests = [r for r in self.test_results if 'Exact Case Email' in r['test']]
        case_insensitive_tests = [r for r in self.test_results if 'Case-Insensitive Test' in r['test']]
        profile_tests = [r for r in self.test_results if 'Profile Access' in r['test']]
        
        if health_tests and health_tests[0]['success']:
            print("✅ Server connectivity to custom domain working")
        else:
            print("❌ Server connectivity issues detected")
        
        if exact_login_tests and exact_login_tests[0]['success']:
            print("✅ Admin login with exact credentials working")
        else:
            print("❌ Admin login with exact credentials failing")
        
        case_insensitive_success = all(r['success'] for r in case_insensitive_tests)
        if case_insensitive_tests and case_insensitive_success:
            print("✅ Case-insensitive email login working correctly")
        else:
            print("❌ Case-insensitive email login not working")
        
        if profile_tests and profile_tests[0]['success']:
            print("✅ JWT token generation and validation working")
        else:
            print("❌ JWT token issues detected")
        
        print()
        if success_rate >= 75:
            print("🎉 AUTHENTICATION SYSTEM STATUS: WORKING")
        else:
            print("⚠️  AUTHENTICATION SYSTEM STATUS: NEEDS ATTENTION")

async def main():
    """Main test execution"""
    tester = AuthenticationTester()
    await tester.run_authentication_tests()

if __name__ == "__main__":
    asyncio.run(main())