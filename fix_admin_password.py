#!/usr/bin/env python3
import asyncio
import motor.motor_asyncio
import bcrypt
import os
from datetime import datetime

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.customer_mind_iq

async def fix_admin_password():
    """Fix the admin account password"""
    
    print("🔧 Fixing admin account password...")
    
    # Create new hash for the password
    password = "CustomerMindIQ2025!"
    salt = bcrypt.gensalt()
    new_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    print(f"   New password hash created: {new_hash[:50]}...")
    
    # Verify the new hash works
    is_valid = bcrypt.checkpw(password.encode('utf-8'), new_hash.encode('utf-8'))
    print(f"   Password verification test: {is_valid}")
    
    if not is_valid:
        print("❌ New hash verification failed!")
        return
    
    # Update the admin account
    result = await db.users.update_one(
        {"email": "admin@customermindiq.com"},
        {
            "$set": {
                "password_hash": new_hash,
                "login_attempts": 0,
                "locked_until": None,
                "last_password_update": datetime.utcnow(),
                "is_active": True
            }
        }
    )
    
    if result.modified_count > 0:
        print("✅ Admin password updated successfully!")
        
        # Verify the update
        admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
        final_check = bcrypt.checkpw(password.encode('utf-8'), admin_user['password_hash'].encode('utf-8'))
        print(f"   Final verification check: {final_check}")
        
        if final_check:
            print("🎉 Admin account is now ready for login!")
            print("   Credentials: admin@customermindiq.com / CustomerMindIQ2025!")
        else:
            print("❌ Final verification failed!")
    else:
        print("❌ Failed to update admin password!")

if __name__ == "__main__":
    asyncio.run(fix_admin_password())