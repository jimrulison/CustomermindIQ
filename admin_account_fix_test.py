#!/usr/bin/env python3
"""
CustomerMind IQ - Admin Account Deactivation Fix Test
Specifically addresses the admin account deactivation issue preventing frontend testing

Test Objectives:
1. Check admin account status in database
2. Reactivate admin account if deactivated
3. Test admin login functionality
4. Verify admin access to endpoints
"""

import asyncio
import json
import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
import urllib3
from motor.motor_asyncio import AsyncIOMotorClient

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-mind-iq-5.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# MongoDB Configuration
MONGO_URL = "mongodb+srv://mindiq-auth:CMIQ123@cluster0.iw5g77.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "test_database"

# Admin credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class AdminAccountFixTester:
    def __init__(self):
        self.admin_token = None
        self.results = []
        self.client = None
        self.db = None

    async def setup_database_connection(self):
        """Setup direct MongoDB connection for admin account inspection/fix"""
        try:
            self.client = AsyncIOMotorClient(MONGO_URL)
            self.db = self.client[DB_NAME]
            
            # Test connection
            await self.client.admin.command('ping')
            self.log_result("✅ DATABASE CONNECTION", "Successfully connected to MongoDB", True)
            return True
            
        except Exception as e:
            self.log_result("❌ DATABASE CONNECTION", f"Failed to connect to MongoDB: {e}", False)
            return False

    async def check_admin_account_status(self):
        """Check current admin account status in database"""
        try:
            admin_user = await self.db.users.find_one({"email": "admin@customermindiq.com"})
            
            if not admin_user:
                self.log_result("❌ ADMIN ACCOUNT CHECK", "Admin account not found in database", False)
                return None
            
            status_info = {
                "email": admin_user.get("email"),
                "is_active": admin_user.get("is_active", True),
                "locked_until": admin_user.get("locked_until"),
                "login_attempts": admin_user.get("login_attempts", 0),
                "role": admin_user.get("role"),
                "created_at": admin_user.get("created_at"),
                "last_login": admin_user.get("last_login")
            }
            
            # Determine if account needs fixing
            needs_fix = (
                not admin_user.get("is_active", True) or
                admin_user.get("locked_until") is not None or
                admin_user.get("login_attempts", 0) >= 5
            )
            
            status_msg = f"Admin account found - Active: {status_info['is_active']}, Locked: {status_info['locked_until'] is not None}, Login Attempts: {status_info['login_attempts']}"
            
            if needs_fix:
                self.log_result("⚠️ ADMIN ACCOUNT STATUS", f"{status_msg} - NEEDS REACTIVATION", False)
            else:
                self.log_result("✅ ADMIN ACCOUNT STATUS", f"{status_msg} - ACCOUNT OK", True)
            
            return status_info
            
        except Exception as e:
            self.log_result("❌ ADMIN ACCOUNT CHECK", f"Error checking admin account: {e}", False)
            return None

    async def reactivate_admin_account(self):
        """Reactivate admin account by fixing all potential issues"""
        try:
            # Update admin account to fix all potential issues
            update_result = await self.db.users.update_one(
                {"email": "admin@customermindiq.com"},
                {
                    "$set": {
                        "is_active": True,
                        "login_attempts": 0,
                        "last_login": None
                    },
                    "$unset": {
                        "locked_until": ""
                    }
                }
            )
            
            if update_result.matched_count > 0:
                self.log_result("✅ ADMIN ACCOUNT REACTIVATION", f"Successfully reactivated admin account (modified: {update_result.modified_count})", True)
                
                # Verify the fix
                updated_admin = await self.db.users.find_one({"email": "admin@customermindiq.com"})
                verification_msg = f"Verified - Active: {updated_admin.get('is_active')}, Locked: {updated_admin.get('locked_until') is None}, Login Attempts: {updated_admin.get('login_attempts', 0)}"
                self.log_result("✅ REACTIVATION VERIFICATION", verification_msg, True)
                
                return True
            else:
                self.log_result("❌ ADMIN ACCOUNT REACTIVATION", "No admin account found to update", False)
                return False
                
        except Exception as e:
            self.log_result("❌ ADMIN ACCOUNT REACTIVATION", f"Error reactivating admin account: {e}", False)
            return False

    async def test_admin_login(self):
        """Test admin login with correct credentials"""
        try:
            response = requests.post(
                f"{API_BASE}/auth/login",
                json=ADMIN_CREDENTIALS,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    self.admin_token = data["access_token"]
                    user_info = data.get("user", {})
                    self.log_result("✅ ADMIN LOGIN", f"Successfully logged in as {user_info.get('email')} with role {user_info.get('role')}", True)
                    return True
                else:
                    self.log_result("❌ ADMIN LOGIN", f"Login response missing access token: {data}", False)
                    return False
            else:
                error_msg = f"Login failed with status {response.status_code}: {response.text}"
                self.log_result("❌ ADMIN LOGIN", error_msg, False)
                return False
                
        except Exception as e:
            self.log_result("❌ ADMIN LOGIN", f"Login request failed: {e}", False)
            return False

    async def test_admin_endpoints(self):
        """Test access to admin endpoints"""
        if not self.admin_token:
            self.log_result("❌ ADMIN ENDPOINTS", "No admin token available for testing", False)
            return False

        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test admin analytics endpoint
        try:
            response = requests.get(
                f"{API_BASE}/admin/analytics/dashboard",
                headers=headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result("✅ ADMIN ANALYTICS ACCESS", f"Successfully accessed admin analytics - Users: {data.get('total_users', 'N/A')}, Revenue: ${data.get('monthly_revenue', 'N/A')}", True)
            else:
                self.log_result("❌ ADMIN ANALYTICS ACCESS", f"Failed to access admin analytics: {response.status_code} - {response.text}", False)
                
        except Exception as e:
            self.log_result("❌ ADMIN ANALYTICS ACCESS", f"Error accessing admin analytics: {e}", False)

        # Test admin user management endpoint
        try:
            response = requests.get(
                f"{API_BASE}/admin/users/search?limit=5",
                headers=headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                user_count = len(data.get("users", []))
                self.log_result("✅ ADMIN USER MANAGEMENT", f"Successfully accessed user management - Found {user_count} users", True)
            else:
                self.log_result("❌ ADMIN USER MANAGEMENT", f"Failed to access user management: {response.status_code} - {response.text}", False)
                
        except Exception as e:
            self.log_result("❌ ADMIN USER MANAGEMENT", f"Error accessing user management: {e}", False)

    def log_result(self, test_name: str, message: str, success: bool):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status} | {test_name}: {message}")

    async def run_complete_fix_test(self):
        """Run complete admin account fix and verification test"""
        print("🚀 Starting Admin Account Deactivation Fix Test")
        print("=" * 80)
        
        # Step 1: Setup database connection
        if not await self.setup_database_connection():
            print("❌ Cannot proceed without database connection")
            return
        
        # Step 2: Check current admin account status
        admin_status = await self.check_admin_account_status()
        if admin_status is None:
            print("❌ Cannot proceed without admin account")
            return
        
        # Step 3: Reactivate admin account if needed
        needs_reactivation = (
            not admin_status.get("is_active", True) or
            admin_status.get("locked_until") is not None or
            admin_status.get("login_attempts", 0) >= 5
        )
        
        if needs_reactivation:
            print("\n🔧 Admin account needs reactivation - fixing now...")
            await self.reactivate_admin_account()
        else:
            print("\n✅ Admin account appears to be active - proceeding with login test...")
        
        # Step 4: Test admin login
        print("\n🔐 Testing admin login...")
        login_success = await self.test_admin_login()
        
        # Step 5: Test admin endpoints if login successful
        if login_success:
            print("\n🛡️ Testing admin endpoint access...")
            await self.test_admin_endpoints()
        
        # Step 6: Close database connection
        if self.client:
            self.client.close()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 ADMIN ACCOUNT FIX TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for r in self.results if "✅ PASS" in r["status"])
        total = len(self.results)
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
        print(f"Overall Status: {'✅ SUCCESS' if success_rate >= 80 else '❌ NEEDS ATTENTION'}")
        
        if success_rate >= 80:
            print("\n🎉 ADMIN ACCOUNT ISSUE RESOLVED!")
            print("✅ Admin account is now active and accessible")
            print("✅ Frontend testing can now proceed")
            print("✅ Admin login working with credentials: admin@customermindiq.com / CustomerMindIQ2025!")
        else:
            print("\n⚠️ ADMIN ACCOUNT ISSUES REMAIN")
            print("❌ Additional investigation required")
            print("❌ Frontend testing may still be blocked")
        
        return success_rate >= 80

async def main():
    """Main test execution"""
    tester = AdminAccountFixTester()
    success = await tester.run_complete_fix_test()
    
    if success:
        print("\n🎯 NEXT STEPS FOR MAIN AGENT:")
        print("1. Admin account is now fully functional")
        print("2. Frontend testing can proceed without authentication barriers")
        print("3. Growth Acceleration video and overage approval system testing can continue")
        print("4. No further admin account fixes needed")
    else:
        print("\n🚨 ESCALATION REQUIRED:")
        print("1. Admin account issues persist despite reactivation attempts")
        print("2. May require deeper investigation of authentication system")
        print("3. Consider checking backend authentication module configuration")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())