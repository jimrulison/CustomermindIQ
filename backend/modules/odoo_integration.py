import os
import xmlrpc.client
import httpx
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum
from dotenv import load_dotenv
import logging
from functools import wraps
import time

# Import auth dependencies
from auth.auth_system import get_current_user, require_role, UserRole, UserProfile, SubscriptionTier

# Load environment variables
load_dotenv()

# MongoDB setup for local tracking
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Router for contact form endpoints
router = APIRouter(tags=["ODOO Integration & Contact Forms"])

# Models for Contact Form
class ContactFormSubmission(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, regex=r"^[\d\-\+\(\)\s]+$")
    company: Optional[str] = Field(None, max_length=100)
    subject: str = Field(..., min_length=5, max_length=200)
    message: str = Field(..., min_length=10, max_length=2000)
    website: Optional[str] = None
    source: str = "website_contact_form"
    
    @validator('website')
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            v = f'https://{v}'
        return v

class ContactFormResponse(BaseModel):
    form_id: str
    name: str
    email: str
    subject: str
    status: str
    odoo_contact_id: Optional[int] = None
    odoo_ticket_id: Optional[int] = None
    submitted_at: datetime
    admin_response: Optional[str] = None
    admin_response_at: Optional[datetime] = None

class AdminResponse(BaseModel):
    message: str = Field(..., min_length=10, max_length=2000)

class ODOOIntegration:
    """
    ODOO ERP Integration for Customer Mind IQ Platform
    Provides real customer data, purchase history, and email system integration
    """
    
    def __init__(self):
        self.url = os.getenv('ODOO_URL')
        self.database = os.getenv('ODOO_DATABASE')
        self.username = os.getenv('ODOO_USERNAME')
        self.password = os.getenv('ODOO_PASSWORD')
        self.api_key = os.getenv('ODOO_API_KEY')
        
        if not all([self.url, self.database, self.username, self.password]):
            raise ValueError("Missing ODOO credentials in environment variables")
        
        # Initialize connection objects
        self.common = None
        self.models = None
        self.uid = None
        
        # Connection status
        self.connected = False
        self.last_connection_attempt = None
        
        # Initialize connection
        self._connect()
    
    def _connect(self):
        """Establish connection to ODOO server"""
        try:
            logger.info(f"Connecting to ODOO at {self.url}")
            
            # Create server proxy objects
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
            
            # Authenticate and get user ID
            self.uid = self.common.authenticate(
                self.database, 
                self.username, 
                self.api_key,  # Use API key instead of password
                {}
            )
            
            if self.uid:
                logger.info(f"Successfully connected to ODOO as user ID: {self.uid}")
                self.connected = True
            else:
                logger.error("ODOO authentication failed")
                self.connected = False
                
        except Exception as e:
            logger.error(f"ODOO connection failed: {str(e)}")
            self.connected = False
            
        self.last_connection_attempt = datetime.now()
    
    def retry_on_failure(max_retries=3, delay=1):
        """Decorator to retry ODOO operations on failure"""
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        if not self.connected:
                            self._connect()
                        
                        if not self.connected:
                            raise ConnectionError("Could not establish ODOO connection")
                        
                        return func(self, *args, **kwargs)
                        
                    except Exception as e:
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                        if attempt == max_retries - 1:
                            raise e
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                        self.connected = False
                        
                return None
            return wrapper
        return decorator
    
    @retry_on_failure(max_retries=3)
    def get_customers(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieve customer data from ODOO res.partner model
        """
        try:
            # Search for customer partners (is_customer=True)
            customer_ids = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'res.partner', 'search',
                [[['is_company', '=', False], ['customer_rank', '>', 0]]],
                {'limit': limit, 'offset': offset}
            )
            
            if not customer_ids:
                return []
            
            # Read customer data
            customers = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'res.partner', 'read',
                [customer_ids],
                {
                    'fields': [
                        'name', 'email', 'phone', 'mobile',
                        'street', 'city', 'state_id', 'country_id',
                        'create_date', 'write_date',
                        'customer_rank', 'supplier_rank',
                        'category_id', 'user_id',
                        'total_invoiced', 'credit_limit'
                    ]
                }
            )
            
            # Transform ODOO data to Customer Mind IQ format
            transformed_customers = []
            for customer in customers:
                transformed_customer = self._transform_customer_data(customer)
                transformed_customers.append(transformed_customer)
            
            logger.info(f"Retrieved {len(transformed_customers)} customers from ODOO")
            return transformed_customers
            
        except Exception as e:
            logger.error(f"Error retrieving customers: {str(e)}")
            return []
    
    @retry_on_failure(max_retries=3)
    def get_customer_purchase_history(self, customer_id: int, days_back: int = 365) -> List[Dict[str, Any]]:
        """
        Get customer's purchase history from ODOO
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Search for sales orders for this customer
            order_ids = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'sale.order', 'search',
                [[
                    ['partner_id', '=', customer_id],
                    ['state', 'in', ['sale', 'done']],
                    ['date_order', '>=', start_date.strftime('%Y-%m-%d')],
                    ['date_order', '<=', end_date.strftime('%Y-%m-%d')]
                ]]
            )
            
            if not order_ids:
                return []
            
            # Read order data
            orders = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'sale.order', 'read',
                [order_ids],
                {
                    'fields': [
                        'name', 'date_order', 'amount_total', 'amount_untaxed',
                        'state', 'currency_id', 'order_line'
                    ]
                }
            )
            
            # Get order line details for each order
            purchase_history = []
            for order in orders:
                order_lines = self._get_order_lines(order['order_line'])
                
                transformed_order = {
                    'order_id': order['name'],
                    'date': order['date_order'],
                    'total_amount': order['amount_total'],
                    'currency': order.get('currency_id', [None, 'USD'])[1] if order.get('currency_id') else 'USD',
                    'status': order['state'],
                    'items': order_lines
                }
                purchase_history.append(transformed_order)
            
            logger.info(f"Retrieved {len(purchase_history)} orders for customer {customer_id}")
            return purchase_history
            
        except Exception as e:
            logger.error(f"Error retrieving purchase history: {str(e)}")
            return []
    
    @retry_on_failure(max_retries=3)
    def _get_order_lines(self, order_line_ids: List[int]) -> List[Dict[str, Any]]:
        """Get detailed order line information"""
        try:
            if not order_line_ids:
                return []
            
            order_lines = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'sale.order.line', 'read',
                [order_line_ids],
                {
                    'fields': [
                        'product_id', 'name', 'product_uom_qty',
                        'price_unit', 'price_subtotal', 'discount'
                    ]
                }
            )
            
            transformed_lines = []
            for line in order_lines:
                product_name = line.get('product_id', [None, 'Unknown Product'])
                if isinstance(product_name, list) and len(product_name) > 1:
                    product_name = product_name[1]
                else:
                    product_name = line.get('name', 'Unknown Product')
                
                transformed_line = {
                    'product_name': product_name,
                    'quantity': line['product_uom_qty'],
                    'unit_price': line['price_unit'],
                    'total_price': line['price_subtotal'],
                    'discount': line.get('discount', 0)
                }
                transformed_lines.append(transformed_line)
            
            return transformed_lines
            
        except Exception as e:
            logger.error(f"Error retrieving order lines: {str(e)}")
            return []
    
    @retry_on_failure(max_retries=3)
    def get_products(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get product catalog from ODOO
        """
        try:
            # Search for active products
            product_ids = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'product.template', 'search',
                [[['active', '=', True], ['sale_ok', '=', True]]],
                {'limit': limit}
            )
            
            if not product_ids:
                return []
            
            # Read product data
            products = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'product.template', 'read',
                [product_ids],
                {
                    'fields': [
                        'name', 'list_price', 'standard_price',
                        'categ_id', 'description_sale',
                        'active', 'type'
                    ]
                }
            )
            
            # Transform product data
            transformed_products = []
            for product in products:
                category_name = product.get('categ_id', [None, 'Uncategorized'])
                if isinstance(category_name, list) and len(category_name) > 1:
                    category_name = category_name[1]
                
                transformed_product = {
                    'product_id': product['id'],
                    'name': product['name'],
                    'price': product['list_price'],
                    'cost': product['standard_price'],
                    'category': category_name,
                    'description': product.get('description_sale', ''),
                    'type': product.get('type', 'product')
                }
                transformed_products.append(transformed_product)
            
            logger.info(f"Retrieved {len(transformed_products)} products from ODOO")
            return transformed_products
            
        except Exception as e:
            logger.error(f"Error retrieving products: {str(e)}")
            return []
    
    @retry_on_failure(max_retries=3)
    def send_email(self, recipient_email: str, subject: str, body: str, template_id: Optional[int] = None) -> bool:
        """
        Send email through ODOO's email system
        """
        try:
            # Create mail message
            mail_data = {
                'subject': subject,
                'body_html': body,
                'email_to': recipient_email,
                'auto_delete': False,
                'state': 'outgoing'
            }
            
            # If template is specified, use it
            if template_id:
                mail_data['mail_template_id'] = template_id
            
            # Create mail record
            mail_id = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'mail.mail', 'create',
                [mail_data]
            )
            
            # Send the mail
            self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'mail.mail', 'send',
                [[mail_id]]
            )
            
            logger.info(f"Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    @retry_on_failure(max_retries=3)
    def create_customer(self, customer_data: Dict[str, Any]) -> Optional[int]:
        """
        Create new customer in ODOO
        """
        try:
            odoo_data = {
                'name': customer_data.get('name', ''),
                'email': customer_data.get('email', ''),
                'phone': customer_data.get('phone', ''),
                'is_company': False,
                'customer_rank': 1,
                'supplier_rank': 0
            }
            
            # Add optional fields if provided
            if customer_data.get('street'):
                odoo_data['street'] = customer_data['street']
            if customer_data.get('city'):
                odoo_data['city'] = customer_data['city']
            
            customer_id = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'res.partner', 'create',
                [odoo_data]
            )
            
            logger.info(f"Created customer with ID: {customer_id}")
            return customer_id
            
        except Exception as e:
            logger.error(f"Error creating customer: {str(e)}")
            return None
    
    def _transform_customer_data(self, odoo_customer: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform ODOO customer data to Customer Mind IQ format
        """
        # Calculate derived fields
        registration_date = odoo_customer.get('create_date', datetime.now().isoformat())
        if isinstance(registration_date, str):
            try:
                reg_date = datetime.fromisoformat(registration_date.replace('Z', '+00:00'))
                days_since_registration = (datetime.now() - reg_date.replace(tzinfo=None)).days
            except:
                days_since_registration = 0
        else:
            days_since_registration = 0
        
        # Generate basic customer intelligence data
        total_spent = odoo_customer.get('total_invoiced', 0)
        
        # Calculate engagement score based on available data
        engagement_score = min(100, max(0, 
            (50 if total_spent > 0 else 0) + 
            (30 if odoo_customer.get('email') else 0) +
            (20 if days_since_registration < 365 else 10)
        ))
        
        transformed = {
            'customer_id': str(odoo_customer['id']),
            'name': odoo_customer.get('name', 'Unknown'),
            'email': odoo_customer.get('email', ''),
            'phone': odoo_customer.get('phone', ''),
            'registration_date': registration_date,
            'total_spent': float(total_spent),
            'total_purchases': 0,  # Will be calculated from purchase history
            'last_purchase_date': None,  # Will be updated from purchase history
            'engagement_score': engagement_score,
            'lifecycle_stage': self._determine_lifecycle_stage(total_spent, days_since_registration),
            'address': {
                'street': odoo_customer.get('street', ''),
                'city': odoo_customer.get('city', ''),
                'state': odoo_customer.get('state_id', [None, ''])[1] if odoo_customer.get('state_id') else '',
                'country': odoo_customer.get('country_id', [None, ''])[1] if odoo_customer.get('country_id') else ''
            },
            'software_owned': [],  # Will be populated from purchase history
            'created_at': datetime.now().isoformat(),
            'updated_at': odoo_customer.get('write_date', datetime.now().isoformat())
        }
        
        return transformed
    
    def _determine_lifecycle_stage(self, total_spent: float, days_since_registration: int) -> str:
        """Determine customer lifecycle stage based on basic metrics"""
        if total_spent == 0:
            return 'new'
        elif total_spent > 1000 and days_since_registration > 90:
            return 'active'
        elif total_spent > 0 and days_since_registration > 180:
            return 'at_risk'
        else:
            return 'active'
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current connection status"""
        return {
            'connected': self.connected,
            'last_attempt': self.last_connection_attempt.isoformat() if self.last_connection_attempt else None,
            'database': self.database,
            'url': self.url,
            'user_id': self.uid
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test ODOO connection and return status"""
        try:
            self._connect()
            
            if self.connected:
                # Test a simple query
                version = self.common.version()
                return {
                    'status': 'success',
                    'connected': True,
                    'version': version,
                    'user_id': self.uid,
                    'message': 'ODOO connection successful'
                }
            else:
                return {
                    'status': 'error',
                    'connected': False,
                    'message': 'Authentication failed'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'connected': False,
                'message': f'Connection failed: {str(e)}'
            }

# Initialize global instance
odoo_integration = ODOOIntegration()