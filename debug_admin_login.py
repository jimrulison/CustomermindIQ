#!/usr/bin/env python3
"""
Debug admin login issue
"""

import asyncio
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Configuration
MONGO_URL = "mongodb+srv://mindiq-auth:CMIQ123@cluster0.iw5g77.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "test_database"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

async def debug_admin_login():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Get admin user
    admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
    
    if not admin_user:
        print("❌ Admin user not found")
        return
    
    print("✅ Admin user found")
    print(f"Email: {admin_user.get('email')}")
    print(f"Is active: {admin_user.get('is_active')}")
    print(f"Role: {admin_user.get('role')}")
    print(f"Login attempts: {admin_user.get('login_attempts', 0)}")
    print(f"Locked until: {admin_user.get('locked_until')}")
    
    # Test password verification
    password = "CustomerMindIQ2025!"
    stored_hash = admin_user.get('password_hash')
    
    if stored_hash:
        print(f"\n🔐 Testing password verification...")
        print(f"Password: {password}")
        print(f"Hash length: {len(stored_hash)}")
        print(f"Hash starts with: {stored_hash[:10]}...")
        
        # Test verification
        is_valid = verify_password(password, stored_hash)
        print(f"Password verification result: {is_valid}")
        
        if not is_valid:
            print("\n🔧 Password verification failed - regenerating hash...")
            new_hash = hash_password(password)
            print(f"New hash: {new_hash[:20]}...")
            
            # Update the password hash
            result = await db.users.update_one(
                {"email": "admin@customermindiq.com"},
                {"$set": {"password_hash": new_hash}}
            )
            
            print(f"Hash update result: {result.modified_count} documents modified")
            
            # Test new hash
            new_verification = verify_password(password, new_hash)
            print(f"New hash verification: {new_verification}")
    else:
        print("❌ No password hash found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_admin_login())