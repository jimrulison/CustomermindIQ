#!/usr/bin/env python3
"""
CustomerMind IQ - Admin Dashboard 500 Error Investigation
Focused testing for specific issues mentioned in review request:

1. Admin Dashboard 500 Error: /api/admin/analytics/dashboard
2. Missing Email Endpoints: /api/email/campaigns and /api/email/providers/current  
3. General Admin Portal Functionality: Test all admin endpoints systematically

Authentication: admin@customermindiq.com / CustomerMindIQ2025!
"""

import asyncio
import json
import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
import urllib3
import traceback

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-success-ai.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials from review request
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class AdminDashboardInvestigator:
    def __init__(self):
        self.admin_token = None
        self.results = []
        self.headers = {}
        
    def log_result(self, test_name: str, success: bool, details: str = "", data: Any = None, status_code: int = None):
        """Log detailed test result with error analysis"""
        status = "✅ WORKING" if success else "❌ FAILING"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "status_code": status_code,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        
        print(f"{status}: {test_name}")
        if status_code:
            print(f"   Status Code: {status_code}")
        if details:
            print(f"   Details: {details}")
        if not success and data:
            print(f"   Error Response: {str(data)[:500]}...")
        print()
        
    def setup_auth_headers(self):
        """Setup authentication headers"""
        if self.admin_token:
            self.headers = {
                "Authorization": f"Bearer {self.admin_token}",
                "Content-Type": "application/json"
            }
        
    async def test_admin_authentication(self):
        """Test admin authentication with exact credentials from review"""
        print("🔐 TESTING ADMIN AUTHENTICATION")
        print("=" * 60)
        
        try:
            response = requests.post(
                f"{API_BASE}/auth/login", 
                json=ADMIN_CREDENTIALS, 
                timeout=30, 
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                user_info = data.get("user", {})
                
                self.log_result(
                    "Admin Authentication", 
                    True, 
                    f"Login successful - Role: {user_info.get('role')}, Email: {user_info.get('email')}", 
                    status_code=response.status_code
                )
                self.setup_auth_headers()
                return True
            else:
                self.log_result(
                    "Admin Authentication", 
                    False, 
                    f"Authentication failed", 
                    response.text,
                    status_code=response.status_code
                )
                return False
                
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Exception: {str(e)}")
            return False
    
    async def investigate_admin_dashboard_500_error(self):
        """PRIMARY ISSUE: Investigate /api/admin/analytics/dashboard 500 error"""
        print("🚨 INVESTIGATING ADMIN DASHBOARD 500 ERROR")
        print("=" * 60)
        
        if not self.admin_token:
            self.log_result("Admin Dashboard Investigation", False, "No admin token available")
            return
        
        try:
            response = requests.get(
                f"{API_BASE}/admin/analytics/dashboard",
                headers=self.headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Admin Analytics Dashboard", 
                    True, 
                    f"Dashboard loaded successfully with {len(data)} data points",
                    status_code=response.status_code
                )
            elif response.status_code == 500:
                # Detailed 500 error analysis
                error_text = response.text
                try:
                    error_json = response.json()
                    error_detail = error_json.get('detail', 'No detail provided')
                except:
                    error_detail = error_text
                
                self.log_result(
                    "Admin Analytics Dashboard", 
                    False, 
                    f"500 Internal Server Error - {error_detail}",
                    error_text,
                    status_code=response.status_code
                )
            else:
                self.log_result(
                    "Admin Analytics Dashboard", 
                    False, 
                    f"Unexpected status code",
                    response.text,
                    status_code=response.status_code
                )
                
        except Exception as e:
            self.log_result("Admin Analytics Dashboard", False, f"Exception: {str(e)}")
    
    async def investigate_missing_email_endpoints(self):
        """PRIMARY ISSUE: Investigate missing email endpoints returning 404"""
        print("📧 INVESTIGATING MISSING EMAIL ENDPOINTS")
        print("=" * 60)
        
        if not self.admin_token:
            self.log_result("Email Endpoints Investigation", False, "No admin token available")
            return
        
        # Test /api/email/campaigns
        try:
            response = requests.get(
                f"{API_BASE}/email/campaigns",
                headers=self.headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Email Campaigns Endpoint", 
                    True, 
                    f"Endpoint exists and returned {len(data) if isinstance(data, list) else 'data'}",
                    status_code=response.status_code
                )
            elif response.status_code == 404:
                self.log_result(
                    "Email Campaigns Endpoint", 
                    False, 
                    "Endpoint not found - missing implementation",
                    response.text,
                    status_code=response.status_code
                )
            else:
                self.log_result(
                    "Email Campaigns Endpoint", 
                    False, 
                    f"Unexpected response",
                    response.text,
                    status_code=response.status_code
                )
                
        except Exception as e:
            self.log_result("Email Campaigns Endpoint", False, f"Exception: {str(e)}")
        
        # Test /api/email/providers/current
        try:
            response = requests.get(
                f"{API_BASE}/email/providers/current",
                headers=self.headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Email Providers Current Endpoint", 
                    True, 
                    f"Endpoint exists and returned provider info",
                    status_code=response.status_code
                )
            elif response.status_code == 404:
                self.log_result(
                    "Email Providers Current Endpoint", 
                    False, 
                    "Endpoint not found - missing implementation",
                    response.text,
                    status_code=response.status_code
                )
            else:
                self.log_result(
                    "Email Providers Current Endpoint", 
                    False, 
                    f"Unexpected response",
                    response.text,
                    status_code=response.status_code
                )
                
        except Exception as e:
            self.log_result("Email Providers Current Endpoint", False, f"Exception: {str(e)}")
    
    async def test_all_admin_endpoints_systematically(self):
        """Test all admin portal endpoints systematically to identify broken links"""
        print("🔧 TESTING ALL ADMIN ENDPOINTS SYSTEMATICALLY")
        print("=" * 60)
        
        if not self.admin_token:
            self.log_result("Admin Endpoints Testing", False, "No admin token available")
            return
        
        # List of admin endpoints to test based on server.py analysis
        admin_endpoints = [
            "/admin/banners",
            "/admin/discounts", 
            "/admin/users",
            "/admin/customers",
            "/admin/announcements",
            "/admin/analytics/dashboard",
            "/admin/user-search",
            "/admin/bulk-discount",
            "/admin/discount-performance",
            "/admin/cohort-analysis",
            "/admin/export/users",
            "/admin/export/discounts",
            "/admin/api-keys",
            "/admin/impersonation/start",
            "/admin/workflows"
        ]
        
        working_endpoints = []
        broken_endpoints = []
        
        for endpoint in admin_endpoints:
            try:
                response = requests.get(
                    f"{API_BASE}{endpoint}",
                    headers=self.headers,
                    timeout=15,
                    verify=False
                )
                
                if response.status_code == 200:
                    working_endpoints.append(endpoint)
                    self.log_result(
                        f"Admin Endpoint: {endpoint}", 
                        True, 
                        "Endpoint accessible and working",
                        status_code=response.status_code
                    )
                elif response.status_code == 404:
                    broken_endpoints.append(endpoint)
                    self.log_result(
                        f"Admin Endpoint: {endpoint}", 
                        False, 
                        "Endpoint not found (404)",
                        status_code=response.status_code
                    )
                elif response.status_code == 500:
                    broken_endpoints.append(endpoint)
                    try:
                        error_data = response.json()
                        error_detail = error_data.get('detail', 'No detail')
                    except:
                        error_detail = response.text[:200]
                    
                    self.log_result(
                        f"Admin Endpoint: {endpoint}", 
                        False, 
                        f"500 Internal Server Error - {error_detail}",
                        status_code=response.status_code
                    )
                else:
                    broken_endpoints.append(endpoint)
                    self.log_result(
                        f"Admin Endpoint: {endpoint}", 
                        False, 
                        f"Unexpected status code",
                        response.text[:200],
                        status_code=response.status_code
                    )
                    
            except Exception as e:
                broken_endpoints.append(endpoint)
                self.log_result(f"Admin Endpoint: {endpoint}", False, f"Exception: {str(e)}")
        
        # Summary
        print(f"\n📊 ADMIN ENDPOINTS SUMMARY:")
        print(f"✅ Working Endpoints: {len(working_endpoints)}")
        print(f"❌ Broken Endpoints: {len(broken_endpoints)}")
        print(f"📈 Success Rate: {len(working_endpoints)}/{len(admin_endpoints)} ({len(working_endpoints)/len(admin_endpoints)*100:.1f}%)")
        
        if working_endpoints:
            print(f"\n✅ WORKING ENDPOINTS:")
            for endpoint in working_endpoints:
                print(f"   - {endpoint}")
        
        if broken_endpoints:
            print(f"\n❌ BROKEN ENDPOINTS:")
            for endpoint in broken_endpoints:
                print(f"   - {endpoint}")
    
    async def test_additional_email_system_endpoints(self):
        """Test additional email system endpoints that might exist"""
        print("📬 TESTING ADDITIONAL EMAIL SYSTEM ENDPOINTS")
        print("=" * 60)
        
        if not self.admin_token:
            return
        
        # Additional email endpoints that might exist
        email_endpoints = [
            "/email/send-simple",
            "/email/stats", 
            "/email/templates",
            "/email/providers",
            "/email/campaigns/create",
            "/email/campaigns/send"
        ]
        
        for endpoint in email_endpoints:
            try:
                response = requests.get(
                    f"{API_BASE}{endpoint}",
                    headers=self.headers,
                    timeout=15,
                    verify=False
                )
                
                if response.status_code == 200:
                    self.log_result(
                        f"Email Endpoint: {endpoint}", 
                        True, 
                        "Endpoint exists and accessible",
                        status_code=response.status_code
                    )
                elif response.status_code == 404:
                    self.log_result(
                        f"Email Endpoint: {endpoint}", 
                        False, 
                        "Endpoint not found",
                        status_code=response.status_code
                    )
                elif response.status_code == 405:
                    self.log_result(
                        f"Email Endpoint: {endpoint}", 
                        True, 
                        "Endpoint exists but wrong method (GET vs POST)",
                        status_code=response.status_code
                    )
                else:
                    self.log_result(
                        f"Email Endpoint: {endpoint}", 
                        False, 
                        f"Status: {response.status_code}",
                        response.text[:200],
                        status_code=response.status_code
                    )
                    
            except Exception as e:
                self.log_result(f"Email Endpoint: {endpoint}", False, f"Exception: {str(e)}")
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n" + "=" * 80)
        print("🎯 ADMIN DASHBOARD INVESTIGATION SUMMARY REPORT")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r['success']])
        failed_tests = total_tests - passed_tests
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   📈 Success Rate: {passed_tests/total_tests*100:.1f}%")
        
        # Critical Issues Analysis
        critical_issues = []
        
        # Check for 500 errors
        dashboard_500_errors = [r for r in self.results if 'Admin Analytics Dashboard' in r['test'] and r['status_code'] == 500]
        if dashboard_500_errors:
            critical_issues.append("🚨 Admin Dashboard 500 Error: /api/admin/analytics/dashboard returning server error")
        
        # Check for missing email endpoints
        missing_email_endpoints = [r for r in self.results if 'Email' in r['test'] and r['status_code'] == 404]
        if missing_email_endpoints:
            critical_issues.append("🚨 Missing Email Endpoints: Email system endpoints not implemented")
        
        # Check for broken admin links
        broken_admin_endpoints = [r for r in self.results if 'Admin Endpoint' in r['test'] and not r['success']]
        if broken_admin_endpoints:
            critical_issues.append(f"🚨 Broken Admin Links: {len(broken_admin_endpoints)} admin endpoints not working")
        
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES IDENTIFIED:")
            for i, issue in enumerate(critical_issues, 1):
                print(f"   {i}. {issue}")
        else:
            print(f"\n✅ NO CRITICAL ISSUES FOUND")
        
        # Detailed Error Analysis
        print(f"\n🔍 DETAILED ERROR ANALYSIS:")
        
        # 500 Errors
        server_errors = [r for r in self.results if r['status_code'] == 500]
        if server_errors:
            print(f"\n   🔥 500 INTERNAL SERVER ERRORS ({len(server_errors)}):")
            for error in server_errors:
                print(f"      - {error['test']}: {error['details']}")
        
        # 404 Errors  
        not_found_errors = [r for r in self.results if r['status_code'] == 404]
        if not_found_errors:
            print(f"\n   🔍 404 NOT FOUND ERRORS ({len(not_found_errors)}):")
            for error in not_found_errors:
                print(f"      - {error['test']}: Missing endpoint")
        
        # Working Features
        working_features = [r for r in self.results if r['success']]
        if working_features:
            print(f"\n   ✅ WORKING FEATURES ({len(working_features)}):")
            for feature in working_features[:5]:  # Show first 5
                print(f"      - {feature['test']}")
            if len(working_features) > 5:
                print(f"      ... and {len(working_features) - 5} more")
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": passed_tests/total_tests*100,
            "critical_issues": critical_issues,
            "server_errors": len(server_errors),
            "not_found_errors": len(not_found_errors)
        }

async def main():
    """Main investigation function"""
    print("🔍 CustomerMind IQ - Admin Dashboard Investigation")
    print("🎯 Focus: 500 errors, missing email endpoints, broken admin links")
    print("🔐 Authentication: admin@customermindiq.com")
    print("=" * 80)
    
    investigator = AdminDashboardInvestigator()
    
    # Step 1: Authenticate as admin
    auth_success = await investigator.test_admin_authentication()
    if not auth_success:
        print("❌ CRITICAL: Admin authentication failed. Cannot proceed with investigation.")
        return
    
    # Step 2: Investigate specific issues from review request
    await investigator.investigate_admin_dashboard_500_error()
    await investigator.investigate_missing_email_endpoints()
    
    # Step 3: Systematic testing of all admin endpoints
    await investigator.test_all_admin_endpoints_systematically()
    
    # Step 4: Test additional email system endpoints
    await investigator.test_additional_email_system_endpoints()
    
    # Step 5: Generate comprehensive summary
    summary = investigator.generate_summary_report()
    
    print(f"\n🎯 INVESTIGATION COMPLETE")
    print(f"📋 Results logged for main agent analysis")
    
    return summary

if __name__ == "__main__":
    asyncio.run(main())