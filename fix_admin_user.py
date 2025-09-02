#!/usr/bin/env python3
"""
Fix admin user subscription tier from 'enterprise' to 'scale'
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")

async def fix_admin_user():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Find admin user
    admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
    
    if admin_user:
        print(f"Found admin user with subscription_tier: {admin_user.get('subscription_tier')}")
        
        # Update subscription tier from 'enterprise' to 'scale'
        result = await db.users.update_one(
            {"email": "admin@customermindiq.com"},
            {
                "$set": {
                    "subscription_tier": "scale",
                    "plan_type": "scale",
                    "billing_cycle": "annual",
                    "subscription_type": "annual"
                }
            }
        )
        
        print(f"Updated admin user: matched={result.matched_count}, modified={result.modified_count}")
        
        # Verify update
        updated_user = await db.users.find_one({"email": "admin@customermindiq.com"})
        print(f"Admin user now has subscription_tier: {updated_user.get('subscription_tier')}")
    else:
        print("Admin user not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_admin_user())