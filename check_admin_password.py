#!/usr/bin/env python3
"""
Check admin password field in database
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Configuration
MONGO_URL = "mongodb+srv://mindiq-auth:CMIQ123@cluster0.iw5g77.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "test_database"

async def check_admin_password():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
    
    if admin_user:
        print("Admin user found:")
        print(f"Email: {admin_user.get('email')}")
        print(f"User ID: {admin_user.get('user_id')}")
        print(f"Has password field: {'password' in admin_user}")
        print(f"Has password_hash field: {'password_hash' in admin_user}")
        print(f"Is active: {admin_user.get('is_active')}")
        print(f"Role: {admin_user.get('role')}")
        
        if 'password' in admin_user:
            print(f"Password field length: {len(admin_user['password'])}")
        if 'password_hash' in admin_user:
            print(f"Password hash field length: {len(admin_user['password_hash'])}")
    else:
        print("Admin user not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_admin_password())