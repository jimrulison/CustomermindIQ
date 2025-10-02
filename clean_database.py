#!/usr/bin/env python3
"""
Database cleanup script for Customer Mind IQ
This script will clean all data from MongoDB collections
"""

import asyncio
import os
from pymongo import MongoClient
from urllib.parse import urlparse
import sys

def get_mongo_connection():
    """Get MongoDB connection from environment"""
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    if not mongo_url:
        print("❌ MONGO_URL not found in environment")
        return None, None
    
    try:
        client = MongoClient(mongo_url)
        db = client[db_name]
        print(f"✅ Connected to MongoDB: {db_name}")
        return client, db
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return None, None

def clean_all_collections(db):
    """Clean all collections in the database"""
    try:
        # Get all collection names
        collections = db.list_collection_names()
        
        if not collections:
            print("📋 No collections found in database")
            return True
        
        print(f"📋 Found {len(collections)} collections: {collections}")
        
        total_documents_deleted = 0
        
        for collection_name in collections:
            collection = db[collection_name]
            
            # Count documents before deletion
            doc_count = collection.count_documents({})
            print(f"🗃️  Collection '{collection_name}': {doc_count} documents")
            
            if doc_count > 0:
                # Delete all documents
                result = collection.delete_many({})
                print(f"   ✅ Deleted {result.deleted_count} documents from '{collection_name}'")
                total_documents_deleted += result.deleted_count
            else:
                print(f"   ℹ️  Collection '{collection_name}' was already empty")
        
        print(f"\n🎯 CLEANUP COMPLETE: Deleted {total_documents_deleted} total documents")
        
        # Verify cleanup
        print("\n🔍 Verifying cleanup...")
        all_empty = True
        for collection_name in collections:
            collection = db[collection_name]
            remaining_count = collection.count_documents({})
            if remaining_count > 0:
                print(f"   ❌ Collection '{collection_name}' still has {remaining_count} documents")
                all_empty = False
            else:
                print(f"   ✅ Collection '{collection_name}' is empty")
        
        if all_empty:
            print("\n🎉 SUCCESS: All collections are now empty!")
            return True
        else:
            print("\n⚠️  WARNING: Some collections still have data")
            return False
            
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return False

def main():
    """Main cleanup function"""
    print("🧹 Starting Customer Mind IQ Database Cleanup...")
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
        print("✅ Loaded environment variables from .env file")
    
    # Connect to MongoDB
    client, db = get_mongo_connection()
    
    if not client or not db:
        print("❌ Cannot proceed without database connection")
        sys.exit(1)
    
    try:
        # Perform cleanup
        success = clean_all_collections(db)
        
        if success:
            print("\n🎉 DATABASE CLEANUP COMPLETED SUCCESSFULLY!")
            print("The Customer Mind IQ application now has a fresh, clean database.")
        else:
            print("\n⚠️  DATABASE CLEANUP COMPLETED WITH WARNINGS")
            print("Some data may still remain in the database.")
            
    except KeyboardInterrupt:
        print("\n⏹️  Cleanup interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during cleanup: {e}")
    finally:
        # Close connection
        if client:
            client.close()
            print("🔌 Database connection closed")

if __name__ == "__main__":
    main()