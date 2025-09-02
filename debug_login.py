#!/usr/bin/env python3
"""
Debug login process
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt
import re

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")

async def debug_login():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    email = "admin@customermindiq.com"
    password = "CustomerMindIQ2025!"
    
    print(f"Debugging login for: {email}")
    print(f"Database: {DB_NAME}")
    print(f"MongoDB URL: {MONGO_URL[:50]}...")
    
    # Case-insensitive email search (like in the auth system)
    email_pattern = re.compile(f"^{re.escape(email)}$", re.IGNORECASE)
    user = await db.users.find_one({"email": email_pattern})
    
    if user:
        print(f"\n✅ User found!")
        print(f"  Email: {user.get('email')}")
        print(f"  Role: {user.get('role')}")
        print(f"  Subscription tier: {user.get('subscription_tier')}")
        print(f"  Is active: {user.get('is_active')}")
        
        # Test password
        stored_hash = user.get("password_hash", "")
        if stored_hash and bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            print("  ✅ Password matches!")
        else:
            print("  ❌ Password doesn't match!")
            
        # Check for problematic fields
        problematic_fields = []
        for k, v in user.items():
            if k == "subscription_tier" and v not in ["free", "launch", "growth", "scale", "white_label", "custom"]:
                problematic_fields.append(f"{k}={v}")
        
        if problematic_fields:
            print(f"  ❌ Problematic fields: {problematic_fields}")
        else:
            print("  ✅ All fields look good!")
            
    else:
        print("❌ User not found!")
        
        # Check if there are any users with similar email
        similar_users = await db.users.find({"email": {"$regex": "admin", "$options": "i"}}).to_list(length=10)
        print(f"Found {len(similar_users)} users with 'admin' in email:")
        for u in similar_users:
            print(f"  - {u.get('email')} (tier: {u.get('subscription_tier')})")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_login())