#!/usr/bin/env python3
"""
Check all admin users
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
import json

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")

async def check_all_admin_users():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Find all admin users
    admin_users = await db.users.find({"email": "admin@customermindiq.com"}).to_list(length=10)
    
    print(f"Found {len(admin_users)} admin users:")
    for i, user in enumerate(admin_users):
        user['_id'] = str(user['_id'])
        print(f"\nAdmin user {i+1}:")
        print(f"  subscription_tier: {user.get('subscription_tier')}")
        print(f"  role: {user.get('role')}")
        print(f"  created_at: {user.get('created_at')}")
    
    # Update all admin users
    result = await db.users.update_many(
        {"email": "admin@customermindiq.com"},
        {
            "$set": {
                "subscription_tier": "scale",
                "plan_type": "scale",
                "billing_cycle": "annual", 
                "subscription_type": "annual",
                "trial_end_date": None
            }
        }
    )
    
    print(f"\nUpdated {result.modified_count} admin users")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_all_admin_users())