#!/usr/bin/env python3
"""
Reset admin password
"""

import asyncio
import os
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

async def reset_admin_password():
    # MongoDB setup
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # New password
        new_password = "CustomerMindIQ2025!"
        hashed_password = hash_password(new_password)
        
        # Update admin password
        result = await db.users.update_one(
            {"email": "admin@customermindiq.com"},
            {"$set": {
                "password_hash": hashed_password,
                "password_changed_at": datetime.utcnow(),
                "last_password_update": datetime.utcnow(),
                "is_active": True,
                "login_attempts": 0,
                "locked_until": None
            }}
        )
        
        if result.modified_count > 0:
            print("✅ Admin password reset successfully!")
            print(f"New password: {new_password}")
        else:
            print("❌ Failed to reset admin password")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(reset_admin_password())