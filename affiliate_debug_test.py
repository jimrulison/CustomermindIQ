#!/usr/bin/env python3
"""
CustomerMind IQ - Affiliate Debug Test
Debug and fix the affiliate login issue
"""

import asyncio
import json
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def debug_affiliate_system():
    """Debug the affiliate system"""
    try:
        # Connect to MongoDB
        MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        DB_NAME = os.getenv("DB_NAME", "test_database")
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        print("🔍 AFFILIATE SYSTEM DEBUG")
        print("=" * 60)
        print(f"MongoDB URL: {MONGO_URL}")
        print(f"Database: {DB_NAME}")
        print("=" * 60)
        
        # Check if affiliates collection exists
        collections = await db.list_collection_names()
        print(f"Available collections: {collections}")
        
        if "affiliates" not in collections:
            print("❌ Affiliates collection does not exist")
            return False
        
        # Get all affiliates
        affiliates = await db.affiliates.find({}).to_list(length=100)
        print(f"\n📊 Total affiliates found: {len(affiliates)}")
        
        # Look for admin affiliate
        admin_affiliate = None
        for affiliate in affiliates:
            print(f"\n👤 Affiliate: {affiliate.get('email')}")
            print(f"   ID: {affiliate.get('affiliate_id')}")
            print(f"   Status: {affiliate.get('status')}")
            print(f"   Name: {affiliate.get('first_name')} {affiliate.get('last_name')}")
            
            if affiliate.get('email') == 'admin@customermindiq.com':
                admin_affiliate = affiliate
        
        if admin_affiliate:
            print(f"\n✅ Found admin affiliate account:")
            print(f"   Email: {admin_affiliate.get('email')}")
            print(f"   Status: {admin_affiliate.get('status')}")
            print(f"   ID: {admin_affiliate.get('affiliate_id')}")
            
            # Approve the account if it's pending
            if admin_affiliate.get('status') == 'pending':
                print(f"\n🔧 Approving admin affiliate account...")
                result = await db.affiliates.update_one(
                    {"email": "admin@customermindiq.com"},
                    {"$set": {"status": "approved"}}
                )
                
                if result.modified_count > 0:
                    print("✅ Admin affiliate account approved successfully")
                    
                    # Verify the update
                    updated_affiliate = await db.affiliates.find_one({"email": "admin@customermindiq.com"})
                    print(f"   New status: {updated_affiliate.get('status')}")
                    return True
                else:
                    print("❌ Failed to update affiliate status")
                    return False
            else:
                print(f"✅ Admin affiliate account already has status: {admin_affiliate.get('status')}")
                return True
        else:
            print("\n❌ Admin affiliate account not found")
            print("   Need to create affiliate account for admin@customermindiq.com")
            return False
            
    except Exception as e:
        print(f"❌ Error debugging affiliate system: {e}")
        return False

def main():
    """Main execution"""
    success = asyncio.run(debug_affiliate_system())
    
    if success:
        print("\n🎉 Affiliate system debug completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Affiliate system debug failed")
        sys.exit(1)

if __name__ == "__main__":
    main()