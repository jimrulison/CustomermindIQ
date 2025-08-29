#!/usr/bin/env python3
import asyncio
import motor.motor_asyncio
import bcrypt
import os

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.customer_mind_iq

async def debug_admin_account():
    """Debug the admin account to see what's wrong with authentication"""
    
    print("🔍 Debugging admin account...")
    
    # Find admin user
    admin_user = await db.users.find_one({"email": "admin@customermindiq.com"})
    
    if not admin_user:
        print("❌ Admin user not found!")
        return
    
    print(f"✅ Admin user found!")
    print(f"   User ID: {admin_user.get('user_id')}")
    print(f"   Email: {admin_user.get('email')}")
    print(f"   Role: {admin_user.get('role')}")
    print(f"   Is Active: {admin_user.get('is_active')}")
    print(f"   Email Verified: {admin_user.get('email_verified')}")
    print(f"   Login Attempts: {admin_user.get('login_attempts', 0)}")
    print(f"   Locked Until: {admin_user.get('locked_until')}")
    print(f"   Created At: {admin_user.get('created_at')}")
    
    # Test password verification
    password_to_test = "CustomerMindIQ2025!"
    stored_hash = admin_user.get('password_hash')
    
    print(f"\n🔐 Testing password verification...")
    print(f"   Password to test: {password_to_test}")
    print(f"   Stored hash length: {len(stored_hash) if stored_hash else 0}")
    
    try:
        # Manual bcrypt verification
        is_valid = bcrypt.checkpw(password_to_test.encode('utf-8'), stored_hash.encode('utf-8'))
        print(f"   Password verification result: {is_valid}")
        
        if not is_valid:
            print("❌ Password verification failed!")
            # Try to create a new hash and see if it matches the pattern
            new_hash = bcrypt.hashpw(password_to_test.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            print(f"   New hash example: {new_hash[:50]}...")
            print(f"   Stored hash: {stored_hash[:50] if stored_hash else 'None'}...")
        else:
            print("✅ Password verification successful!")
            
    except Exception as e:
        print(f"❌ Error during password verification: {e}")
    
    # Check for any issues with the account
    issues = []
    if not admin_user.get('is_active', True):
        issues.append("Account is not active")
    if admin_user.get('locked_until'):
        issues.append(f"Account is locked until {admin_user.get('locked_until')}")
    if admin_user.get('login_attempts', 0) >= 5:
        issues.append(f"Too many failed login attempts: {admin_user.get('login_attempts')}")
    
    if issues:
        print(f"\n⚠️ Account Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print(f"\n✅ No account issues found")

if __name__ == "__main__":
    asyncio.run(debug_admin_account())