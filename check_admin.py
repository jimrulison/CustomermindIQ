#!/usr/bin/env python3
"""
Check admin user details
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def check_admin():
    # MongoDB setup
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # Find admin user
        admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
        
        if admin_user:
            print("Admin user found:")
            print(f"  Email: {admin_user.get('email')}")
            print(f"  User ID: {admin_user.get('user_id')}")
            print(f"  Role: {admin_user.get('role')}")
            print(f"  Is Active: {admin_user.get('is_active')}")
            print(f"  Locked Until: {admin_user.get('locked_until')}")
            print(f"  Login Attempts: {admin_user.get('login_attempts', 0)}")
            print(f"  Created At: {admin_user.get('created_at')}")
            print(f"  Last Login: {admin_user.get('last_login')}")
            
            # Check if there are any fields that might be causing issues
            print("\nAll fields:")
            for key, value in admin_user.items():
                if key != 'password':  # Don't print password
                    print(f"  {key}: {value}")
                    
        else:
            print("❌ Admin user not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_admin())