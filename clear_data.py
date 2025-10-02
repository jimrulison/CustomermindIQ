#!/usr/bin/env python3
"""
Database cleanup script for Customer Mind IQ - Clear all data
"""

import os
from pymongo import MongoClient

def clear_database():
    """Clear all data from MongoDB database"""
    print("🧹 Starting Database Data Cleanup...")
    print("=" * 50)
    
    # Load environment variables from .env file
    env_path = '/app/backend/.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"').strip("'")
                    os.environ[key] = value
        print("✅ Loaded environment variables")
    
    # Get MongoDB connection details
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    if not mongo_url:
        print("❌ MONGO_URL not found in environment")
        return False
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_url)
        db = client[db_name]
        print(f"✅ Connected to MongoDB: {db_name}")
        
        # Get all collection names
        collections = db.list_collection_names()
        
        if not collections:
            print("📋 Database is already empty - no collections found")
            return True
        
        print(f"📋 Found {len(collections)} collections to clear:")
        for i, collection_name in enumerate(collections, 1):
            print(f"   {i}. {collection_name}")
        
        print("\n🗑️  Starting data cleanup...")
        
        total_documents_deleted = 0
        
        # Clear each collection
        for collection_name in collections:
            collection = db[collection_name]
            
            # Count documents before deletion
            doc_count = collection.count_documents({})
            
            if doc_count > 0:
                # Delete all documents
                result = collection.delete_many({})
                print(f"   ✅ Cleared {result.deleted_count:,} documents from '{collection_name}'")
                total_documents_deleted += result.deleted_count
            else:
                print(f"   ⚪ Collection '{collection_name}' was already empty")
        
        print(f"\n🎯 CLEANUP COMPLETE!")
        print(f"   Total documents deleted: {total_documents_deleted:,}")
        
        # Verification
        print("\n🔍 Verifying cleanup...")
        all_empty = True
        total_remaining = 0
        
        for collection_name in collections:
            collection = db[collection_name]
            remaining_count = collection.count_documents({})
            total_remaining += remaining_count
            
            if remaining_count > 0:
                print(f"   ⚠️  '{collection_name}': {remaining_count} documents remaining")
                all_empty = False
            else:
                print(f"   ✅ '{collection_name}': Empty")
        
        if all_empty:
            print(f"\n🎉 SUCCESS: All {len(collections)} collections are now empty!")
            print("   Database has been completely cleared and is ready for fresh data.")
        else:
            print(f"\n⚠️  WARNING: {total_remaining} documents still remain in the database")
        
        # Close connection
        client.close()
        print("🔌 Database connection closed")
        
        return all_empty
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return False

if __name__ == "__main__":
    success = clear_database()
    if success:
        print("\n✨ Database cleanup completed successfully!")
    else:
        print("\n💥 Database cleanup failed!")