#!/usr/bin/env python3
"""
Test user validation
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
import sys
sys.path.append('/app/backend')

from auth.auth_system import UserProfile, UserRole, SubscriptionTier, SubscriptionType

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")

async def test_user_validation():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Find admin user
    user = await db.users.find_one({"email": "admin@customermindiq.com"})
    
    if user:
        print("Raw user data:")
        for k, v in user.items():
            if k != "password_hash":
                print(f"  {k}: {v} ({type(v)})")
        
        print("\nTrying to create UserProfile...")
        try:
            # Filter out password_hash and _id
            user_data = {k: v for k, v in user.items() if k not in ["password_hash", "_id"]}
            user_profile = UserProfile(**user_data)
            print("✅ UserProfile created successfully!")
            print(f"subscription_tier: {user_profile.subscription_tier}")
        except Exception as e:
            print(f"❌ UserProfile validation failed: {e}")
            
            # Try to identify the problematic field
            print("\nTesting individual fields:")
            for k, v in user_data.items():
                try:
                    if k == "role":
                        UserRole(v)
                        print(f"  ✅ {k}: {v}")
                    elif k == "subscription_tier":
                        SubscriptionTier(v)
                        print(f"  ✅ {k}: {v}")
                    elif k == "subscription_type":
                        if v:
                            SubscriptionType(v)
                        print(f"  ✅ {k}: {v}")
                    else:
                        print(f"  ✅ {k}: {v}")
                except Exception as field_error:
                    print(f"  ❌ {k}: {v} - {field_error}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(test_user_validation())