"""
Customer Mind IQ - Stripe Connector
Universal connector for Stripe payment and subscription data
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import aiohttp
import json
from .base_connector import BaseConnector, UniversalCustomer, UniversalTransaction, UniversalProduct

class StripeConnector(BaseConnector):
    """
    Stripe connector for Customer Mind IQ
    Extracts customer, payment, and subscription data from Stripe
    """
    
    def __init__(self, credentials: Dict[str, str]):
        """
        Initialize Stripe connector
        Args:
            credentials: Dictionary containing 'api_key' for Stripe
        """
        super().__init__(credentials)
        self.stripe_key = credentials.get('api_key', '')
        self.base_url = "https://api.stripe.com/v1"
        
    def get_platform_name(self) -> str:
        return "stripe"
    
    async def test_connection(self) -> bool:
        """Test Stripe API connection"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.stripe_key}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                async with session.get(f"{self.base_url}/account", headers=headers) as response:
                    if response.status == 200:
                        print("✅ Stripe connection successful")
                        return True
                    else:
                        print(f"❌ Stripe connection failed: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ Stripe connection error: {e}")
            return False
    
    async def sync_customers(self, limit: int = 100) -> List[UniversalCustomer]:
        """Sync customers from Stripe"""
        try:
            customers = []
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.stripe_key}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                # Get customers from Stripe
                url = f"{self.base_url}/customers?limit={limit}"
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        print(f"Failed to fetch Stripe customers: {response.status}")
                        return []
                    
                    data = await response.json()
                    stripe_customers = data.get('data', [])
                    
                    print(f"Found {len(stripe_customers)} customers in Stripe")
                    
                    for stripe_customer in stripe_customers:
                        # Get customer's payment history to calculate total spent
                        total_spent = await self._get_customer_total_spent(session, headers, stripe_customer['id'])
                        total_orders = await self._get_customer_total_orders(session, headers, stripe_customer['id'])
                        last_payment = await self._get_customer_last_payment_date(session, headers, stripe_customer['id'])
                        
                        universal_customer = UniversalCustomer(
                            customer_id=self.generate_universal_customer_id(stripe_customer['id']),
                            platform_customer_id=stripe_customer['id'],
                            platform_name=self.platform_name,
                            email=self.normalize_email(stripe_customer.get('email', '')),
                            name=stripe_customer.get('name') or stripe_customer.get('description', ''),
                            created_date=datetime.fromtimestamp(stripe_customer['created']) if stripe_customer.get('created') else None,
                            total_spent=total_spent,
                            total_orders=total_orders,
                            last_order_date=last_payment,
                            status="active" if not stripe_customer.get('delinquent', False) else "at_risk",
                            metadata={
                                'stripe_customer_id': stripe_customer['id'],
                                'currency': stripe_customer.get('currency', 'usd'),
                                'delinquent': stripe_customer.get('delinquent', False),
                                'default_source': stripe_customer.get('default_source'),
                                'invoice_prefix': stripe_customer.get('invoice_prefix')
                            }
                        )
                        
                        customers.append(universal_customer)
            
            print(f"✅ Synced {len(customers)} customers from Stripe")
            return customers
            
        except Exception as e:
            print(f"❌ Error syncing Stripe customers: {e}")
            return []
    
    async def _get_customer_total_spent(self, session: aiohttp.ClientSession, headers: Dict, customer_id: str) -> float:
        """Calculate total amount spent by customer"""
        try:
            url = f"{self.base_url}/charges?customer={customer_id}&limit=100"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    charges = data.get('data', [])
                    total = sum(charge['amount'] for charge in charges if charge.get('paid', False)) / 100  # Convert from cents
                    return total
        except Exception as e:
            print(f"Error getting customer total spent: {e}")
        return 0.0
    
    async def _get_customer_total_orders(self, session: aiohttp.ClientSession, headers: Dict, customer_id: str) -> int:
        """Get total number of successful orders/payments"""
        try:
            url = f"{self.base_url}/charges?customer={customer_id}&limit=100"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    charges = data.get('data', [])
                    return len([charge for charge in charges if charge.get('paid', False)])
        except Exception as e:
            print(f"Error getting customer total orders: {e}")
        return 0
    
    async def _get_customer_last_payment_date(self, session: aiohttp.ClientSession, headers: Dict, customer_id: str) -> Optional[datetime]:
        """Get date of customer's last successful payment"""
        try:
            url = f"{self.base_url}/charges?customer={customer_id}&limit=1"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    charges = data.get('data', [])
                    if charges and charges[0].get('paid', False):
                        return datetime.fromtimestamp(charges[0]['created'])
        except Exception as e:
            print(f"Error getting last payment date: {e}")
        return None
    
    async def sync_transactions(self, days_back: int = 30, limit: int = 1000) -> List[UniversalTransaction]:
        """Sync recent transactions from Stripe"""
        try:
            transactions = []
            start_date = datetime.now() - timedelta(days=days_back)
            start_timestamp = int(start_date.timestamp())
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.stripe_key}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                # Get charges (payments) from Stripe
                url = f"{self.base_url}/charges?created[gte]={start_timestamp}&limit={limit}"
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        print(f"Failed to fetch Stripe charges: {response.status}")
                        return []
                    
                    data = await response.json()
                    charges = data.get('data', [])
                    
                    print(f"Found {len(charges)} charges in Stripe")
                    
                    for charge in charges:
                        if charge.get('customer'):  # Only include charges with customer info
                            transaction = UniversalTransaction(
                                transaction_id=self.generate_universal_transaction_id(charge['id']),
                                platform_transaction_id=charge['id'],
                                platform_name=self.platform_name,
                                customer_id=self.generate_universal_customer_id(charge['customer']),
                                amount=charge['amount'] / 100,  # Convert from cents
                                currency=charge['currency'].upper(),
                                transaction_date=datetime.fromtimestamp(charge['created']),
                                transaction_type="purchase" if charge.get('paid', False) else "failed",
                                product_ids=[],  # Stripe charges don't directly contain product info
                                status="completed" if charge.get('paid', False) else "failed",
                                metadata={
                                    'stripe_charge_id': charge['id'],
                                    'payment_method': charge.get('payment_method_details', {}).get('type', 'unknown'),
                                    'description': charge.get('description', ''),
                                    'receipt_url': charge.get('receipt_url'),
                                    'failure_code': charge.get('failure_code'),
                                    'failure_message': charge.get('failure_message')
                                }
                            )
                            
                            transactions.append(transaction)
            
            print(f"✅ Synced {len(transactions)} transactions from Stripe")
            return transactions
            
        except Exception as e:
            print(f"❌ Error syncing Stripe transactions: {e}")
            return []
    
    async def sync_products(self, limit: int = 100) -> List[UniversalProduct]:
        """Sync products from Stripe (using Products API)"""
        try:
            products = []
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.stripe_key}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                # Get products from Stripe
                url = f"{self.base_url}/products?limit={limit}&active=true"
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        print(f"Failed to fetch Stripe products: {response.status}")
                        return []
                    
                    data = await response.json()
                    stripe_products = data.get('data', [])
                    
                    print(f"Found {len(stripe_products)} products in Stripe")
                    
                    for product in stripe_products:
                        # Get default price for the product
                        default_price = await self._get_product_default_price(session, headers, product['id'])
                        
                        universal_product = UniversalProduct(
                            product_id=self.generate_universal_product_id(product['id']),
                            platform_product_id=product['id'],
                            platform_name=self.platform_name,
                            name=product.get('name', ''),
                            category=product.get('metadata', {}).get('category'),
                            price=default_price.get('amount', 0) / 100 if default_price else 0.0,
                            currency=default_price.get('currency', 'usd').upper() if default_price else 'USD',
                            description=product.get('description', ''),
                            metadata={
                                'stripe_product_id': product['id'],
                                'active': product.get('active', True),
                                'type': product.get('type', 'service'),
                                'url': product.get('url'),
                                'images': product.get('images', []),
                                'default_price_id': default_price.get('id') if default_price else None
                            }
                        )
                        
                        products.append(universal_product)
            
            print(f"✅ Synced {len(products)} products from Stripe")
            return products
            
        except Exception as e:
            print(f"❌ Error syncing Stripe products: {e}")
            return []
    
    async def _get_product_default_price(self, session: aiohttp.ClientSession, headers: Dict, product_id: str) -> Optional[Dict]:
        """Get default price for a Stripe product"""
        try:
            url = f"{self.base_url}/prices?product={product_id}&active=true&limit=1"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    prices = data.get('data', [])
                    return prices[0] if prices else None
        except Exception as e:
            print(f"Error getting product price: {e}")
        return None
    
    async def get_subscription_data(self) -> List[Dict[str, Any]]:
        """Get subscription data for recurring revenue analysis"""
        try:
            subscriptions = []
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.stripe_key}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                url = f"{self.base_url}/subscriptions?limit=100&status=all"
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        stripe_subscriptions = data.get('data', [])
                        
                        for sub in stripe_subscriptions:
                            subscription_data = {
                                'subscription_id': sub['id'],
                                'customer_id': self.generate_universal_customer_id(sub['customer']),
                                'status': sub['status'],
                                'current_period_start': datetime.fromtimestamp(sub['current_period_start']),
                                'current_period_end': datetime.fromtimestamp(sub['current_period_end']),
                                'created': datetime.fromtimestamp(sub['created']),
                                'cancel_at_period_end': sub.get('cancel_at_period_end', False),
                                'canceled_at': datetime.fromtimestamp(sub['canceled_at']) if sub.get('canceled_at') else None,
                                'trial_end': datetime.fromtimestamp(sub['trial_end']) if sub.get('trial_end') else None,
                                'metadata': sub.get('metadata', {})
                            }
                            subscriptions.append(subscription_data)
            
            print(f"✅ Found {len(subscriptions)} subscriptions in Stripe")
            return subscriptions
            
        except Exception as e:
            print(f"❌ Error getting Stripe subscriptions: {e}")
            return []