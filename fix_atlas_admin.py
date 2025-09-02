#!/usr/bin/env python3
"""
Fix admin user in the Atlas database (test_database)
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Use the actual environment variables from backend
MONGO_URL = "mongodb+srv://mindiq-auth:CMIQ123@cluster0.iw5g77.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "test_database"

async def fix_atlas_admin():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Find admin user in Atlas database
    admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
    
    if admin_user:
        print(f"Found admin user in Atlas DB with subscription_tier: {admin_user.get('subscription_tier')}")
        
        # Update subscription tier from 'enterprise' to 'scale'
        result = await db.users.update_one(
            {"email": "admin@customermindiq.com"},
            {
                "$set": {
                    "subscription_tier": "scale",
                    "plan_type": "scale",
                    "billing_cycle": "annual",
                    "subscription_type": "annual",
                    "trial_end_date": None,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        print(f"Updated admin user: matched={result.matched_count}, modified={result.modified_count}")
        
        # Verify update
        updated_user = await db.users.find_one({"email": "admin@customermindiq.com"})
        print(f"Admin user now has subscription_tier: {updated_user.get('subscription_tier')}")
    else:
        print("Admin user not found in Atlas database")
        
        # List all users to see what's there
        all_users = await db.users.find({}).to_list(length=10)
        print(f"Found {len(all_users)} users in Atlas database:")
        for user in all_users:
            print(f"  - {user.get('email')} (tier: {user.get('subscription_tier')})")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_atlas_admin())