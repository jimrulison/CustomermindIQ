"""
Customer Mind IQ - Odoo Connector  
Universal connector for Odoo ERP customer and sales data
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import xmlrpc.client
from .base_connector import BaseConnector, UniversalCustomer, UniversalTransaction, UniversalProduct

class OdooConnector(BaseConnector):
    """
    Odoo connector for Customer Mind IQ
    Extracts customer, sales, and product data from Odoo ERP
    """
    
    def __init__(self, credentials: Dict[str, str]):
        """
        Initialize Odoo connector
        Args:
            credentials: Dictionary containing 'url', 'database', 'username', 'password'
        """
        super().__init__(credentials)
        self.url = credentials.get('url', '')
        self.database = credentials.get('database', '')
        self.username = credentials.get('username', '')
        self.password = credentials.get('password', '')
        self.uid = None
        self.common = None
        self.models = None
        
    def get_platform_name(self) -> str:
        return "odoo"
    
    async def test_connection(self) -> bool:
        """Test Odoo connection and authentication"""
        try:
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = self.common.authenticate(
                self.database, self.username, self.password, {}
            )
            
            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                print("✅ Odoo connection successful")
                return True
            else:
                print("❌ Odoo authentication failed")
                return False
                
        except Exception as e:
            print(f"❌ Odoo connection error: {e}")
            return False
    
    async def sync_customers(self, limit: int = 100) -> List[UniversalCustomer]:
        """Sync customers from Odoo"""
        try:
            customers = []
            
            if not await self.test_connection():
                print("Cannot connect to Odoo")
                return []
            
            # Search for customers (contacts that are not companies and have email)
            customer_domain = [
                ('is_company', '=', False),
                ('email', '!=', False),
                ('customer_rank', '>', 0)  # Only customers, not vendors
            ]
            
            customer_ids = self.models.execute_kw(
                self.database, self.uid, self.password,
                'res.partner', 'search', [customer_domain],
                {'limit': limit}
            )
            
            if not customer_ids:
                print("No customers found in Odoo")
                return []
            
            # Get customer details
            odoo_customers = self.models.execute_kw(
                self.database, self.uid, self.password,
                'res.partner', 'read', [customer_ids],
                {'fields': ['name', 'email', 'phone', 'create_date', 'category_id', 'is_company', 'parent_id']}
            )
            
            print(f"Found {len(odoo_customers)} customers in Odoo")
            
            for odoo_customer in odoo_customers:
                # Get customer's sales data
                sales_data = await self._get_customer_sales_data(odoo_customer['id'])
                
                # Convert Odoo date format to datetime
                created_date = None
                if odoo_customer.get('create_date'):
                    try:
                        created_date = datetime.fromisoformat(odoo_customer['create_date'].replace('Z', '+00:00'))
                    except:
                        created_date = datetime.now()
                
                universal_customer = UniversalCustomer(
                    customer_id=self.generate_universal_customer_id(str(odoo_customer['id'])),
                    platform_customer_id=str(odoo_customer['id']),
                    platform_name=self.platform_name,
                    email=self.normalize_email(odoo_customer.get('email', '')),
                    name=odoo_customer.get('name', ''),
                    created_date=created_date,
                    total_spent=sales_data['total_spent'],
                    total_orders=sales_data['total_orders'],
                    last_order_date=sales_data['last_order_date'],
                    status=sales_data['status'],
                    metadata={
                        'odoo_partner_id': odoo_customer['id'],
                        'phone': odoo_customer.get('phone', ''),
                        'category_ids': odoo_customer.get('category_id', []),
                        'is_company': odoo_customer.get('is_company', False),
                        'parent_id': odoo_customer.get('parent_id'),
                        'products_purchased': sales_data['products_purchased']
                    }
                )
                
                customers.append(universal_customer)
            
            print(f"✅ Synced {len(customers)} customers from Odoo")
            return customers
            
        except Exception as e:
            print(f"❌ Error syncing Odoo customers: {e}")
            return []
    
    async def _get_customer_sales_data(self, partner_id: int) -> Dict[str, Any]:
        """Get sales data for a specific customer from Odoo"""
        try:
            # Get sales orders for this customer
            order_domain = [
                ('partner_id', '=', partner_id),
                ('state', 'in', ['sale', 'done'])  # Confirmed and done orders
            ]
            
            order_ids = self.models.execute_kw(
                self.database, self.uid, self.password,
                'sale.order', 'search', [order_domain]
            )
            
            total_spent = 0.0
            total_orders = len(order_ids)
            last_order_date = None
            products_purchased = []
            
            if order_ids:
                # Get order details
                orders = self.models.execute_kw(
                    self.database, self.uid, self.password,
                    'sale.order', 'read', [order_ids],
                    {'fields': ['amount_total', 'date_order', 'order_line', 'state']}
                )
                
                # Calculate totals
                total_spent = sum(order.get('amount_total', 0) for order in orders)
                
                # Get most recent order date
                order_dates = [order.get('date_order') for order in orders if order.get('date_order')]
                if order_dates:
                    try:
                        latest_date_str = max(order_dates)
                        last_order_date = datetime.fromisoformat(latest_date_str.replace('Z', '+00:00'))
                    except:
                        last_order_date = None
                
                # Get product information from order lines
                all_line_ids = []
                for order in orders:
                    if order.get('order_line'):
                        all_line_ids.extend(order['order_line'])
                
                if all_line_ids:
                    lines = self.models.execute_kw(
                        self.database, self.uid, self.password,
                        'sale.order.line', 'read', [all_line_ids],
                        {'fields': ['product_id', 'name', 'product_uom_qty', 'price_unit']}
                    )
                    
                    for line in lines:
                        if line.get('product_id'):
                            product_name = line['product_id'][1] if isinstance(line['product_id'], list) else str(line['product_id'])
                            if product_name not in products_purchased:
                                products_purchased.append(product_name)
            
            # Determine customer status based on activity
            status = "active"
            if last_order_date:
                days_since_last_order = (datetime.now() - last_order_date).days
                if days_since_last_order > 365:
                    status = "inactive"
                elif days_since_last_order > 180:
                    status = "at_risk"
            elif total_orders == 0:
                status = "prospect"
            
            return {
                'total_spent': total_spent,
                'total_orders': total_orders,
                'last_order_date': last_order_date,
                'status': status,
                'products_purchased': products_purchased[:10]  # Limit to top 10 products
            }
            
        except Exception as e:
            print(f"Error getting sales data for customer {partner_id}: {e}")
            return {
                'total_spent': 0.0,
                'total_orders': 0,
                'last_order_date': None,
                'status': 'unknown',
                'products_purchased': []
            }
    
    async def sync_transactions(self, days_back: int = 30, limit: int = 1000) -> List[UniversalTransaction]:
        """Sync recent transactions from Odoo"""
        try:
            transactions = []
            
            if not await self.test_connection():
                print("Cannot connect to Odoo")
                return []
            
            # Calculate date range
            start_date = datetime.now() - timedelta(days=days_back)
            start_date_str = start_date.strftime('%Y-%m-%d')
            
            # Search for recent sales orders
            order_domain = [
                ('date_order', '>=', start_date_str),
                ('state', 'in', ['sale', 'done'])
            ]
            
            order_ids = self.models.execute_kw(
                self.database, self.uid, self.password,
                'sale.order', 'search', [order_domain],
                {'limit': limit}
            )
            
            if not order_ids:
                print("No recent orders found in Odoo")
                return []
            
            # Get order details
            orders = self.models.execute_kw(
                self.database, self.uid, self.password,
                'sale.order', 'read', [order_ids],
                {'fields': ['name', 'partner_id', 'amount_total', 'currency_id', 'date_order', 'state', 'order_line']}
            )
            
            print(f"Found {len(orders)} recent orders in Odoo")
            
            for order in orders:
                # Get product IDs from order lines
                product_ids = []
                if order.get('order_line'):
                    lines = self.models.execute_kw(
                        self.database, self.uid, self.password,
                        'sale.order.line', 'read', [order['order_line']],
                        {'fields': ['product_id']}
                    )
                    
                    for line in lines:
                        if line.get('product_id'):
                            product_id = line['product_id'][0] if isinstance(line['product_id'], list) else line['product_id']
                            product_ids.append(self.generate_universal_product_id(str(product_id)))
                
                # Convert order date
                transaction_date = datetime.now()
                if order.get('date_order'):
                    try:
                        transaction_date = datetime.fromisoformat(order['date_order'].replace('Z', '+00:00'))
                    except:
                        pass
                
                # Get currency
                currency = 'USD'
                if order.get('currency_id') and isinstance(order['currency_id'], list):
                    currency = order['currency_id'][1] if len(order['currency_id']) > 1 else 'USD'
                
                transaction = UniversalTransaction(
                    transaction_id=self.generate_universal_transaction_id(str(order['id'])),
                    platform_transaction_id=str(order['id']),
                    platform_name=self.platform_name,
                    customer_id=self.generate_universal_customer_id(str(order['partner_id'][0])),
                    amount=order.get('amount_total', 0.0),
                    currency=currency.upper(),
                    transaction_date=transaction_date,
                    transaction_type="purchase",
                    product_ids=product_ids,
                    status="completed" if order.get('state') == 'done' else "confirmed",
                    metadata={
                        'odoo_order_id': order['id'],
                        'odoo_order_name': order.get('name', ''),
                        'partner_name': order['partner_id'][1] if isinstance(order['partner_id'], list) else '',
                        'order_state': order.get('state', ''),
                        'line_count': len(order.get('order_line', []))
                    }
                )
                
                transactions.append(transaction)
            
            print(f"✅ Synced {len(transactions)} transactions from Odoo")
            return transactions
            
        except Exception as e:
            print(f"❌ Error syncing Odoo transactions: {e}")
            return []
    
    async def sync_products(self, limit: int = 100) -> List[UniversalProduct]:
        """Sync products from Odoo"""
        try:
            products = []
            
            if not await self.test_connection():
                print("Cannot connect to Odoo")
                return []
            
            # Search for active products that can be sold
            product_domain = [
                ('sale_ok', '=', True),  # Can be sold
                ('active', '=', True)    # Is active
            ]
            
            product_ids = self.models.execute_kw(
                self.database, self.uid, self.password,
                'product.product', 'search', [product_domain],
                {'limit': limit}
            )
            
            if not product_ids:
                print("No products found in Odoo")
                return []
            
            # Get product details
            odoo_products = self.models.execute_kw(
                self.database, self.uid, self.password,
                'product.product', 'read', [product_ids],
                {'fields': ['name', 'list_price', 'currency_id', 'categ_id', 'description', 'active', 'default_code']}
            )
            
            print(f"Found {len(odoo_products)} products in Odoo")
            
            for product in odoo_products:
                # Get currency
                currency = 'USD'
                if product.get('currency_id') and isinstance(product['currency_id'], list):
                    currency = product['currency_id'][1] if len(product['currency_id']) > 1 else 'USD'
                
                # Get category
                category = None
                if product.get('categ_id') and isinstance(product['categ_id'], list):
                    category = product['categ_id'][1] if len(product['categ_id']) > 1 else None
                
                universal_product = UniversalProduct(
                    product_id=self.generate_universal_product_id(str(product['id'])),
                    platform_product_id=str(product['id']),
                    platform_name=self.platform_name,
                    name=product.get('name', ''),
                    category=category,
                    price=product.get('list_price', 0.0),
                    currency=currency.upper(),
                    description=product.get('description', ''),
                    metadata={
                        'odoo_product_id': product['id'],
                        'default_code': product.get('default_code', ''),
                        'active': product.get('active', True),
                        'category_id': product.get('categ_id')
                    }
                )
                
                products.append(universal_product)
            
            print(f"✅ Synced {len(products)} products from Odoo")
            return products
            
        except Exception as e:
            print(f"❌ Error syncing Odoo products: {e}")
            return []
    
    async def get_invoice_data(self) -> List[Dict[str, Any]]:
        """Get invoice data for additional customer insights"""
        try:
            if not await self.test_connection():
                return []
            
            # Search for customer invoices
            invoice_domain = [
                ('move_type', '=', 'out_invoice'),  # Customer invoices
                ('state', '=', 'posted')           # Posted invoices
            ]
            
            invoice_ids = self.models.execute_kw(
                self.database, self.uid, self.password,
                'account.move', 'search', [invoice_domain],
                {'limit': 500}
            )
            
            if not invoice_ids:
                return []
            
            invoices = self.models.execute_kw(
                self.database, self.uid, self.password,
                'account.move', 'read', [invoice_ids],
                {'fields': ['name', 'partner_id', 'amount_total', 'invoice_date', 'payment_state', 'currency_id']}
            )
            
            invoice_data = []
            for invoice in invoices:
                invoice_info = {
                    'invoice_id': invoice['id'],
                    'invoice_name': invoice.get('name', ''),
                    'customer_id': self.generate_universal_customer_id(str(invoice['partner_id'][0])),
                    'amount': invoice.get('amount_total', 0.0),
                    'date': invoice.get('invoice_date'),
                    'payment_state': invoice.get('payment_state', 'not_paid'),
                    'currency': invoice.get('currency_id', [None, 'USD'])[1] if invoice.get('currency_id') else 'USD'
                }
                invoice_data.append(invoice_info)
            
            print(f"✅ Found {len(invoice_data)} invoices in Odoo")
            return invoice_data
            
        except Exception as e:
            print(f"❌ Error getting Odoo invoices: {e}")
            return []