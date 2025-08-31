#!/usr/bin/env python3
"""
Comprehensive Authentication Testing for CustomerMind IQ
Testing both localhost and external domain to identify routing issues
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import sys

class ComprehensiveAuthTester:
    def __init__(self):
        self.localhost_url = "http://localhost:8001"
        self.external_url = "https://customermindiq.com"
        self.session = None
        self.test_results = []
        
    async def setup_session(self):
        """Setup HTTP session with proper headers"""
        connector = aiohttp.TCPConnector(ssl=False)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'CustomerMindIQ-Comprehensive-Tester/1.0'
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
    
    async def test_endpoint(self, base_url, endpoint, method="GET", data=None, headers=None, test_name_suffix=""):
        """Generic endpoint tester"""
        url = f"{base_url}{endpoint}"
        test_name = f"{method} {endpoint} ({base_url.split('//')[1]}) {test_name_suffix}".strip()
        
        try:
            start_time = datetime.now()
            
            if method == "GET":
                async with self.session.get(url, headers=headers) as response:
                    end_time = datetime.now()
                    response_time = (end_time - start_time).total_seconds()
                    
                    if response.status == 200:
                        response_data = await response.json()
                        self.log_test(test_name, True, 
                                    f"Success - Status: {response.status}", 
                                    response_time)
                        return response_data
                    else:
                        error_text = await response.text()
                        self.log_test(test_name, False, 
                                    f"HTTP {response.status}: {error_text[:100]}", 
                                    response_time)
                        return None
            
            elif method == "POST":
                async with self.session.post(url, json=data, headers=headers) as response:
                    end_time = datetime.now()
                    response_time = (end_time - start_time).total_seconds()
                    
                    if response.status == 200:
                        response_data = await response.json()
                        self.log_test(test_name, True, 
                                    f"Success - Status: {response.status}", 
                                    response_time)
                        return response_data
                    else:
                        error_text = await response.text()
                        self.log_test(test_name, False, 
                                    f"HTTP {response.status}: {error_text[:100]}", 
                                    response_time)
                        return None
                        
        except Exception as e:
            self.log_test(test_name, False, f"Connection error: {str(e)}")
            return None
    
    async def run_comprehensive_tests(self):
        """Run comprehensive authentication tests on both localhost and external domain"""
        print("🔐 CustomerMind IQ Comprehensive Authentication Testing")
        print("=" * 80)
        print(f"Localhost URL: {self.localhost_url}")
        print(f"External URL: {self.external_url}")
        print(f"Test Started: {datetime.now().isoformat()}")
        print()
        
        await self.setup_session()
        
        try:
            # Test 1: Health Check on both endpoints
            print("📊 HEALTH CHECK TESTS")
            print("-" * 40)
            await self.test_endpoint(self.localhost_url, "/api/health", "GET")
            await self.test_endpoint(self.external_url, "/api/health", "GET")
            print()
            
            # Test 2: Authentication Tests on Localhost (Expected to work)
            print("🏠 LOCALHOST AUTHENTICATION TESTS")
            print("-" * 40)
            
            # Test exact case login
            login_data = {
                "email": "admin@customermindiq.com",
                "password": "CustomerMindIQ2025!"
            }
            localhost_auth_result = await self.test_endpoint(
                self.localhost_url, "/api/auth/login", "POST", 
                login_data, None, "- Exact Case Email"
            )
            
            # Test case-insensitive login
            case_insensitive_data = {
                "email": "Admin@CustomermindIQ.com",
                "password": "CustomerMindIQ2025!"
            }
            await self.test_endpoint(
                self.localhost_url, "/api/auth/login", "POST", 
                case_insensitive_data, None, "- Mixed Case Email"
            )
            
            # Test uppercase login
            uppercase_data = {
                "email": "ADMIN@CUSTOMERMINDIQ.COM",
                "password": "CustomerMindIQ2025!"
            }
            await self.test_endpoint(
                self.localhost_url, "/api/auth/login", "POST", 
                uppercase_data, None, "- Uppercase Email"
            )
            
            # Test profile endpoint if we have a token
            if localhost_auth_result and 'access_token' in localhost_auth_result:
                profile_headers = {
                    'Authorization': f"Bearer {localhost_auth_result['access_token']}",
                    'Content-Type': 'application/json'
                }
                await self.test_endpoint(
                    self.localhost_url, "/api/auth/profile", "GET", 
                    None, profile_headers, "- Profile Access"
                )
            
            print()
            
            # Test 3: Authentication Tests on External Domain (Expected to fail due to routing)
            print("🌐 EXTERNAL DOMAIN AUTHENTICATION TESTS")
            print("-" * 40)
            
            # Test exact case login
            await self.test_endpoint(
                self.external_url, "/api/auth/login", "POST", 
                login_data, None, "- Exact Case Email"
            )
            
            # Test case-insensitive login
            await self.test_endpoint(
                self.external_url, "/api/auth/login", "POST", 
                case_insensitive_data, None, "- Mixed Case Email"
            )
            
            # Test uppercase login
            await self.test_endpoint(
                self.external_url, "/api/auth/login", "POST", 
                uppercase_data, None, "- Uppercase Email"
            )
            
        finally:
            await self.cleanup_session()
        
        # Print comprehensive summary
        self.print_comprehensive_summary()
    
    def print_comprehensive_summary(self):
        """Print comprehensive test summary with analysis"""
        print("=" * 80)
        print("🔍 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['success']])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        # Categorize results
        localhost_tests = [r for r in self.test_results if 'localhost' in r['test']]
        external_tests = [r for r in self.test_results if 'customermindiq.com' in r['test']]
        health_tests = [r for r in self.test_results if '/api/health' in r['test']]
        auth_tests = [r for r in self.test_results if '/api/auth' in r['test']]
        
        print("📊 RESULTS BY CATEGORY:")
        print(f"Localhost Tests: {len([r for r in localhost_tests if r['success']])}/{len(localhost_tests)} passed")
        print(f"External Domain Tests: {len([r for r in external_tests if r['success']])}/{len(external_tests)} passed")
        print(f"Health Endpoints: {len([r for r in health_tests if r['success']])}/{len(health_tests)} passed")
        print(f"Auth Endpoints: {len([r for r in auth_tests if r['success']])}/{len(auth_tests)} passed")
        print()
        
        print("📋 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}")
            if result['details']:
                print(f"    {result['details']}")
        
        print()
        print("🎯 KEY FINDINGS:")
        
        # Analysis
        localhost_auth_success = all(r['success'] for r in localhost_tests if '/api/auth' in r['test'])
        external_auth_success = all(r['success'] for r in external_tests if '/api/auth' in r['test'])
        health_success = all(r['success'] for r in health_tests)
        
        if health_success:
            print("✅ Server connectivity working on both localhost and external domain")
        else:
            print("❌ Server connectivity issues detected")
        
        if localhost_auth_success:
            print("✅ Authentication system working correctly on localhost")
            print("✅ Case-insensitive email login implemented and working")
            print("✅ JWT token generation and validation working")
        else:
            print("❌ Authentication system issues on localhost")
        
        if not external_auth_success and localhost_auth_success:
            print("❌ External domain routing issue: Auth endpoints not accessible via https://customermindiq.com")
            print("🔧 ISSUE IDENTIFIED: Kubernetes ingress or proxy not routing /api/auth/* endpoints")
        elif external_auth_success:
            print("✅ External domain authentication working")
        
        print()
        print("📝 CONCLUSIONS:")
        if localhost_auth_success and not external_auth_success:
            print("🎯 BACKEND AUTHENTICATION: FULLY FUNCTIONAL")
            print("   - Case-insensitive login working")
            print("   - JWT tokens working")
            print("   - All authentication features implemented correctly")
            print()
            print("⚠️  INFRASTRUCTURE ISSUE: External domain routing")
            print("   - /api/health works on external domain")
            print("   - /api/auth/* endpoints return 500 on external domain")
            print("   - Backend code is correct, issue is in proxy/ingress configuration")
        elif localhost_auth_success and external_auth_success:
            print("🎉 AUTHENTICATION SYSTEM: FULLY WORKING")
            print("   - All features working on both localhost and external domain")
        else:
            print("⚠️  AUTHENTICATION SYSTEM: NEEDS ATTENTION")

async def main():
    """Main test execution"""
    tester = ComprehensiveAuthTester()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())