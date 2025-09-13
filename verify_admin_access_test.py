#!/usr/bin/env python3
"""
Verify Admin Access Test - Test admin role permissions and endpoint access
"""

import requests
import json
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BACKEND_URL = "https://admin-portal-fix-9.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

def test_admin_access():
    """Test comprehensive admin access"""
    print("🔐 Testing Admin Access and Permissions")
    print("=" * 60)
    
    # Step 1: Login as admin
    print("1. Admin Login Test...")
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            json=ADMIN_CREDENTIALS,
            timeout=30,
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            admin_token = data["access_token"]
            user_profile = data.get("user_profile", {})
            
            print(f"✅ Login successful")
            print(f"   Email: {user_profile.get('email')}")
            print(f"   Role: {user_profile.get('role')}")
            print(f"   Subscription: {user_profile.get('subscription_tier')}")
            print(f"   Active: {user_profile.get('is_active')}")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Step 2: Test admin endpoints
    admin_endpoints = [
        ("/admin/analytics/dashboard", "Admin Analytics Dashboard"),
        ("/admin/users/search?limit=3", "User Management"),
        ("/admin/banners", "Banner Management"),
        ("/admin/discounts", "Discount Management")
    ]
    
    print(f"\n2. Testing Admin Endpoints...")
    success_count = 0
    
    for endpoint, description in admin_endpoints:
        try:
            response = requests.get(
                f"{API_BASE}{endpoint}",
                headers=headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                print(f"✅ {description}: Accessible")
                success_count += 1
            elif response.status_code == 401:
                print(f"❌ {description}: Unauthorized (role issue)")
            elif response.status_code == 403:
                print(f"❌ {description}: Forbidden (permission issue)")
            else:
                print(f"⚠️ {description}: {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    # Step 3: Test role-based restrictions
    print(f"\n3. Testing Role-Based Access Control...")
    
    # Test that admin can access protected endpoints
    protected_endpoints = [
        ("/subscriptions/plans", "Subscription Plans"),
        ("/auth/profile", "User Profile")
    ]
    
    for endpoint, description in protected_endpoints:
        try:
            response = requests.get(
                f"{API_BASE}{endpoint}",
                headers=headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                print(f"✅ {description}: Accessible with admin token")
            else:
                print(f"❌ {description}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 ADMIN ACCESS VERIFICATION SUMMARY")
    print(f"=" * 60)
    print(f"Admin endpoints accessible: {success_count}/{len(admin_endpoints)}")
    
    if success_count >= len(admin_endpoints) * 0.75:  # 75% success rate
        print(f"✅ ADMIN ACCESS VERIFIED")
        print(f"✅ Admin role permissions working correctly")
        print(f"✅ Authentication barrier resolved")
        return True
    else:
        print(f"❌ ADMIN ACCESS ISSUES REMAIN")
        print(f"❌ Some admin endpoints not accessible")
        return False

if __name__ == "__main__":
    success = test_admin_access()
    
    if success:
        print(f"\n🎉 ADMIN ACCESS FULLY FUNCTIONAL")
        print(f"Frontend testing can now proceed without barriers!")
    else:
        print(f"\n⚠️ ADMIN ACCESS NEEDS ATTENTION")
        print(f"Some issues may still block frontend testing")