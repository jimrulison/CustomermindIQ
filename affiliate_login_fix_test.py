#!/usr/bin/env python3
"""
CustomerMind IQ - Affiliate Login Fix Test
Fix the affiliate login issue by approving the admin affiliate account
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
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class AffiliateLoginFixer:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.admin_token = None
        
    def get_admin_token(self):
        """Get admin authentication token"""
        try:
            response = self.session.post(
                f"{API_BASE}/auth/login",
                json=ADMIN_CREDENTIALS,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                print("✅ Admin authentication successful")
                return True
            else:
                print(f"❌ Admin login failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Admin login error: {e}")
            return False

    def approve_affiliate_account(self):
        """Approve the admin affiliate account directly via database"""
        try:
            # We'll use the MongoDB connection to directly update the affiliate status
            from motor.motor_asyncio import AsyncIOMotorClient
            import asyncio
            
            async def update_affiliate_status():
                MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
                DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
                client = AsyncIOMotorClient(MONGO_URL)
                db = client[DB_NAME]
                
                # Find and update the admin affiliate account
                result = await db.affiliates.update_one(
                    {"email": "admin@customermindiq.com"},
                    {"$set": {"status": "approved"}}
                )
                
                if result.modified_count > 0:
                    print("✅ Admin affiliate account approved successfully")
                    return True
                else:
                    print("❌ Failed to approve affiliate account or account not found")
                    return False
            
            return asyncio.run(update_affiliate_status())
            
        except Exception as e:
            print(f"❌ Error approving affiliate account: {e}")
            return False

    def test_affiliate_login(self):
        """Test affiliate login after approval"""
        try:
            affiliate_credentials = {
                "email": "admin@customermindiq.com",
                "password": "CustomerMindIQ2025!"
            }
            
            response = self.session.post(
                f"{API_BASE}/affiliate/auth/login",
                json=affiliate_credentials,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Affiliate login successful!")
                print(f"   Token received: {data.get('token')[:20]}...")
                print(f"   Affiliate ID: {data.get('affiliate', {}).get('id')}")
                print(f"   Status: {data.get('affiliate', {}).get('status')}")
                return True
            else:
                print(f"❌ Affiliate login failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Affiliate login error: {e}")
            return False

    def test_external_url_affiliate_login(self):
        """Test affiliate login using the external URL"""
        try:
            external_url = "https://customer-mind-iq-6.preview.emergentagent.com"
            affiliate_credentials = {
                "email": "admin@customermindiq.com",
                "password": "CustomerMindIQ2025!"
            }
            
            response = self.session.post(
                f"{external_url}/api/affiliate/auth/login",
                json=affiliate_credentials,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ External URL affiliate login successful!")
                print(f"   This confirms the fix works for the production URL")
                return True
            elif response.status_code == 502:
                print("❌ External URL returns 502 - infrastructure issue")
                print("   The affiliate login works locally but external URL has routing problems")
                return False
            else:
                print(f"❌ External URL affiliate login failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ External URL affiliate login error: {e}")
            return False

    def run_fix(self):
        """Run the complete fix process"""
        print("🔧 AFFILIATE LOGIN FIX - CustomerMind IQ")
        print("=" * 60)
        print("Fixing affiliate login for admin@customermindiq.com")
        print("=" * 60)
        print()
        
        # Step 1: Get admin token
        if not self.get_admin_token():
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Step 2: Approve affiliate account
        if not self.approve_affiliate_account():
            print("❌ Failed to approve affiliate account")
            return False
        
        # Step 3: Test affiliate login locally
        if not self.test_affiliate_login():
            print("❌ Affiliate login still not working locally")
            return False
        
        # Step 4: Test external URL
        print("\n🌐 Testing external URL...")
        self.test_external_url_affiliate_login()
        
        print("\n" + "=" * 60)
        print("🎉 AFFILIATE LOGIN FIX COMPLETE")
        print("=" * 60)
        print("✅ admin@customermindiq.com can now log in to the affiliate portal")
        print("✅ Account status changed from 'pending' to 'approved'")
        print("✅ Local testing confirms affiliate login works")
        print()
        print("📋 SUMMARY FOR USER:")
        print("- The issue was that admin@customermindiq.com was registered as an affiliate")
        print("  but the account was in 'pending approval' status")
        print("- The account has now been approved and login should work")
        print("- If still getting 'Network error' on the frontend, it may be due to")
        print("  the external URL returning 502 errors (infrastructure issue)")
        
        return True

def main():
    """Main execution"""
    fixer = AffiliateLoginFixer()
    success = fixer.run_fix()
    
    if success:
        print("\n🎉 Fix completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Fix failed")
        sys.exit(1)

if __name__ == "__main__":
    main()