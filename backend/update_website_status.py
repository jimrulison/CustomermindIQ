#!/usr/bin/env python3
"""
Update existing websites from pending_verification to active status
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def update_website_status():
    # MongoDB setup
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # Update all websites with pending_verification status to active
        result = await db.user_websites.update_many(
            {"status": "pending_verification"},
            {"$set": {"status": "active"}}
        )
        
        print(f"✅ Updated {result.modified_count} websites from 'pending_verification' to 'active' status")
        
        # Show current websites
        cursor = db.user_websites.find({})
        websites = await cursor.to_list(length=None)
        
        print(f"\n📋 Current websites in database:")
        for website in websites:
            print(f"  • {website.get('website_name', 'Unnamed')} ({website.get('domain', 'No domain')}) - Status: {website.get('status', 'Unknown')}")
            
    except Exception as e:
        print(f"❌ Error updating website status: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(update_website_status())