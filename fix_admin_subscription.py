#!/usr/bin/env python3
"""
Fix admin subscription tier issue
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Configuration
MONGO_URL = "mongodb+srv://mindiq-auth:CMIQ123@cluster0.iw5g77.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "test_database"

async def fix_admin_subscription():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Get admin user
    admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
    
    if admin_user:
        print(f"Current subscription_tier: {admin_user.get('subscription_tier')}")
        
        # Update to a valid subscription tier
        result = await db.users.update_one(
            {"email": "admin@customermindiq.com"},
            {
                "$set": {
                    "subscription_tier": "custom",  # Valid enum value for admin
                    "is_active": True,
                    "login_attempts": 0
                },
                "$unset": {
                    "locked_until": ""
                }
            }
        )
        
        print(f"Update result: {result.modified_count} documents modified")
        
        # Verify the fix
        updated_admin = await db.users.find_one({"email": "admin@customermindiq.com"})
        print(f"New subscription_tier: {updated_admin.get('subscription_tier')}")
        print(f"Is active: {updated_admin.get('is_active')}")
    else:
        print("Admin user not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_admin_subscription())