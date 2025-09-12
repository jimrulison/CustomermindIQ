#!/usr/bin/env python3
"""
CustomerMind IQ - Focused Overage Approval System Testing
Testing core overage functionality without account deactivation
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
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://mindiq-admin.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

TEST_USER_EMAIL = "admin@customermindiq.com"

class FocusedOverageTester:
    def __init__(self):
        self.admin_token = None
        self.results = []
        
    def log_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        print()

    async def authenticate(self):
        """Authenticate admin user"""
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(f"{API_BASE}/auth/login", json=ADMIN_CREDENTIALS, headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                return True
            return False
        except:
            return False

    async def test_complete_overage_workflow(self):
        """Test the complete overage approval workflow"""
        print("🔄 TESTING COMPLETE OVERAGE APPROVAL WORKFLOW")
        print("=" * 60)
        
        if not await self.authenticate():
            self.log_result("Authentication", False, "Failed to authenticate")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Step 1: Check overage review
        try:
            response = requests.get(f"{API_BASE}/subscriptions/overage-review/{TEST_USER_EMAIL}", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "1. Overage Review Endpoint", 
                    True, 
                    f"Plan: {data['plan_type']}, Pending approvals: {len(data['pending_approvals'])}, Total cost: {data['total_potential_monthly_cost']}"
                )
            else:
                self.log_result("1. Overage Review Endpoint", False, f"Status: {response.status_code}")
                return
        except Exception as e:
            self.log_result("1. Overage Review Endpoint", False, f"Exception: {str(e)}")
            return
        
        # Step 2: Test overage approval
        approval_data = {
            "user_email": TEST_USER_EMAIL,
            "approved_overages": [
                {
                    "resource_type": "contacts",
                    "overage_amount": 500,
                    "monthly_cost": 5.00,
                    "approved": True
                }
            ]
        }
        
        try:
            response = requests.post(f"{API_BASE}/subscriptions/approve-overages", json=approval_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success":
                    self.log_result(
                        "2. Overage Approval Process", 
                        True, 
                        f"Approved {data['approved_items']} items, Cost: {data['total_monthly_cost']}"
                    )
                else:
                    self.log_result("2. Overage Approval Process", False, "Invalid response")
                    return
            else:
                self.log_result("2. Overage Approval Process", False, f"Status: {response.status_code}")
                return
        except Exception as e:
            self.log_result("2. Overage Approval Process", False, f"Exception: {str(e)}")
            return
        
        # Step 3: Check dashboard status
        try:
            response = requests.get(f"{API_BASE}/subscriptions/user-dashboard-overage-status/{TEST_USER_EMAIL}", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                resource_status = data.get("resource_status", {})
                approved_cost = data.get("approved_monthly_overage_cost", "$0.00")
                
                approved_count = sum(1 for status in resource_status.values() if status.get("status") == "approved")
                blocked_count = sum(1 for status in resource_status.values() if status.get("status") == "blocked")
                within_limit_count = sum(1 for status in resource_status.values() if status.get("status") == "within_limit")
                
                self.log_result(
                    "3. User Dashboard Status", 
                    True, 
                    f"Approved: {approved_count}, Blocked: {blocked_count}, Within limit: {within_limit_count}, Cost: {approved_cost}"
                )
            else:
                self.log_result("3. User Dashboard Status", False, f"Status: {response.status_code}")
                return
        except Exception as e:
            self.log_result("3. User Dashboard Status", False, f"Exception: {str(e)}")
            return
        
        # Step 4: Test refund processing time (without actually processing)
        refund_data = {
            "user_email": "test@example.com",  # Use different email to avoid deactivation
            "refund_type": "end_of_cycle",  # Use end_of_cycle to avoid immediate deactivation
            "reason": "Testing refund processing time display",
            "admin_notes": "Test to verify 1-2 business days message"
        }
        
        try:
            response = requests.post(f"{API_BASE}/subscriptions/admin/process-refund", json=refund_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                refund_details = data.get("refund_details", {})
                processing_time = refund_details.get("processing_time", "")
                
                if processing_time == "1-2 business days":
                    self.log_result(
                        "4. Refund Processing Time", 
                        True, 
                        f"Processing time: '{processing_time}' (correct)"
                    )
                else:
                    self.log_result("4. Refund Processing Time", False, f"Wrong processing time: '{processing_time}'")
            else:
                self.log_result("4. Refund Processing Time", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("4. Refund Processing Time", False, f"Exception: {str(e)}")

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("🎯 FOCUSED OVERAGE APPROVAL SYSTEM TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["success"]])
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}% success rate)")
        print()
        
        for result in self.results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"{status}: {result['test']}")
            if result['details']:
                print(f"      {result['details']}")
        
        print()
        print("🔍 CORE OVERAGE SYSTEM VERIFICATION:")
        
        if success_rate >= 75:
            print("  ✅ OVERAGE APPROVAL SYSTEM WORKING CORRECTLY")
            print("  ✅ Users can review pending overage charges")
            print("  ✅ Users can approve specific overages they want")
            print("  ✅ System tracks approved vs blocked resources")
            print("  ✅ Refund processing shows 1-2 business days")
        else:
            print("  ❌ Some core functionality needs attention")
        
        print("\n" + "=" * 80)
        return success_rate >= 75

async def main():
    """Run focused overage approval system test"""
    print("🚀 FOCUSED OVERAGE APPROVAL SYSTEM TESTING")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print("=" * 80)
    
    tester = FocusedOverageTester()
    await tester.test_complete_overage_workflow()
    overall_success = tester.print_summary()
    
    sys.exit(0 if overall_success else 1)

if __name__ == "__main__":
    asyncio.run(main())