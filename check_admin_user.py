#!/usr/bin/env python3
"""
Check admin user data structure
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
import json

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")

async def check_admin_user():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Find admin user
    admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
    
    if admin_user:
        print("Admin user data:")
        # Convert ObjectId to string for JSON serialization
        admin_user['_id'] = str(admin_user['_id'])
        print(json.dumps(admin_user, indent=2, default=str))
    else:
        print("Admin user not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_admin_user())