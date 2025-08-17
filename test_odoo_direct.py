#!/usr/bin/env python3
"""
Direct ODOO Connection Test
"""

import os
import xmlrpc.client
from dotenv import load_dotenv

load_dotenv()

def test_odoo_connection():
    """Test direct ODOO connection"""
    
    url = os.getenv("ODOO_URL")
    database = os.getenv("ODOO_DATABASE") 
    username = os.getenv("ODOO_USERNAME")
    password = os.getenv("ODOO_PASSWORD")
    
    print("🔍 Testing ODOO Connection Directly")
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Database: {database}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
    print("=" * 50)
    
    try:
        # Test 1: Basic connection to common endpoint
        print("\n1️⃣ Testing basic connection to /xmlrpc/2/common...")
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        
        # Test version info
        version_info = common.version()
        print(f"✅ Connection successful!")
        print(f"   ODOO Version: {version_info}")
        
        # Test 2: Authentication
        print(f"\n2️⃣ Testing authentication...")
        uid = common.authenticate(database, username, password, {})
        
        if uid:
            print(f"✅ Authentication successful!")
            print(f"   User ID: {uid}")
            
            # Test 3: Access to object endpoint
            print(f"\n3️⃣ Testing object access...")
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            
            # Test simple query
            partner_count = models.execute_kw(
                database, uid, password,
                'res.partner', 'search_count', [[]]
            )
            print(f"✅ Object access successful!")
            print(f"   Total partners in database: {partner_count}")
            
            # Test 4: Customer query
            print(f"\n4️⃣ Testing customer query...")
            customer_domain = [
                ('is_company', '=', False),
                ('email', '!=', False),
                ('customer_rank', '>', 0)
            ]
            
            customer_ids = models.execute_kw(
                database, uid, password,
                'res.partner', 'search', [customer_domain],
                {'limit': 5}
            )
            
            if customer_ids:
                print(f"✅ Customer query successful!")
                print(f"   Found {len(customer_ids)} customers")
                
                # Get customer details
                customers = models.execute_kw(
                    database, uid, password,
                    'res.partner', 'read', [customer_ids],
                    {'fields': ['name', 'email', 'create_date']}
                )
                
                print(f"   Sample customers:")
                for customer in customers[:3]:
                    print(f"   - {customer['name']} ({customer['email']})")
                    
                return True, f"Successfully connected and found {len(customer_ids)} customers"
            else:
                print(f"⚠️  No customers found with the specified criteria")
                return True, "Connected but no customers found"
                
        else:
            print(f"❌ Authentication failed!")
            return False, "Authentication failed"
            
    except xmlrpc.client.ProtocolError as e:
        print(f"❌ Protocol Error: {e}")
        print(f"   Error Code: {e.errcode}")
        print(f"   Error Message: {e.errmsg}")
        return False, f"Protocol Error: {e.errcode} - {e.errmsg}"
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False, f"Connection Error: {str(e)}"

if __name__ == "__main__":
    success, message = test_odoo_connection()
    print(f"\n{'='*50}")
    print(f"🎯 FINAL RESULT: {'SUCCESS' if success else 'FAILED'}")
    print(f"📝 Message: {message}")
    print(f"{'='*50}")