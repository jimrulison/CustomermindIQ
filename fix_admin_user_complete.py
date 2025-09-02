#!/usr/bin/env python3
"""
Fix admin user to have all required fields
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")

async def fix_admin_user():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Update admin user with all required fields
    result = await db.users.update_one(
        {"email": "admin@customermindiq.com"},
        {
            "$set": {
                "subscription_tier": "scale",
                "plan_type": "scale", 
                "billing_cycle": "annual",
                "subscription_type": "annual",
                "trial_end_date": None,  # Admin doesn't need trial
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    print(f"Updated admin user: matched={result.matched_count}, modified={result.modified_count}")
    
    # Verify update
    updated_user = await db.users.find_one({"email": "admin@customermindiq.com"})
    print(f"Admin user subscription_tier: {updated_user.get('subscription_tier')}")
    print(f"Admin user subscription_type: {updated_user.get('subscription_type')}")
    print(f"Admin user trial_end_date: {updated_user.get('trial_end_date')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_admin_user())