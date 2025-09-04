#!/usr/bin/env python3
"""
Reactivate admin user for testing
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def reactivate_admin():
    # MongoDB setup
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # Find admin user
        admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
        
        if admin_user:
            print(f"Found admin user: {admin_user['email']}")
            print(f"Current status - Active: {admin_user.get('is_active', False)}")
            
            # Reactivate the admin user
            result = await db.users.update_one(
                {"email": "admin@customermindiq.com"},
                {"$set": {"is_active": True}}
            )
            
            if result.modified_count > 0:
                print("✅ Admin user reactivated successfully!")
            else:
                print("⚠️ Admin user was already active or update failed")
                
            # Verify the update
            updated_admin = await db.users.find_one({"email": "admin@customermindiq.com"})
            print(f"Updated status - Active: {updated_admin.get('is_active', False)}")
            
        else:
            print("❌ Admin user not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(reactivate_admin())