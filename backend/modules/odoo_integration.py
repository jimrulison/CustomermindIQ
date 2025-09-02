import os
import xmlrpc.client
import httpx
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
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
    phone: Optional[str] = Field(None, pattern=r"^[\d\-\+\(\)\s]+$")
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
        self.url = os.getenv('ODOO_URL', 'https://your-odoo-instance.com')
        self.database = os.getenv('ODOO_DATABASE', 'main')
        self.username = os.getenv('ODOO_USERNAME', 'admin')
        self.password = os.getenv('ODOO_PASSWORD', 'admin')
        self.api_key = "a69407b31a27a482e5dc4534e56c8b30378cd7fa"  # User provided API key
        
        # For testing, allow missing credentials
        logger.info(f"Initializing ODOO integration with API key: {self.api_key[:20]}...")
        
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

# Contact Form Endpoints
@router.post("/contact-form/submit")
async def submit_contact_form(
    form_data: ContactFormSubmission,
    background_tasks: BackgroundTasks
):
    """
    Submit contact form - creates contact in ODOO and support ticket
    Available to all website visitors (no authentication required)
    """
    
    form_id = str(uuid.uuid4())
    
    try:
        # Store form submission locally for admin tracking
        form_record = {
            "form_id": form_id,
            "name": form_data.name,
            "email": form_data.email,
            "phone": form_data.phone,
            "company": form_data.company,
            "subject": form_data.subject,
            "message": form_data.message,
            "website": form_data.website,
            "source": form_data.source,
            "status": "pending",
            "submitted_at": datetime.utcnow(),
            "odoo_contact_id": None,
            "odoo_ticket_id": None,
            "admin_response": None,
            "admin_response_at": None
        }
        
        await db.contact_form_submissions.insert_one(form_record)
        
        # Process ODOO integration in background
        background_tasks.add_task(
            process_contact_form_odoo_integration,
            form_id,
            form_data.dict()
        )
        
        return {
            "status": "success",
            "message": "Thank you for contacting us! We'll get back to you soon.",
            "form_id": form_id,
            "reference": form_id[-8:]  # Short reference for customer
        }
        
    except Exception as e:
        logger.error(f"Contact form submission error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit contact form")

async def process_contact_form_odoo_integration(form_id: str, form_data: Dict[str, Any]):
    """Background task to process ODOO integration"""
    try:
        # Create contact in ODOO
        odoo_contact_id = odoo_integration.create_customer({
            'name': form_data['name'],
            'email': form_data['email'],
            'phone': form_data.get('phone', ''),
            'company': form_data.get('company', ''),
            'website': form_data.get('website', ''),
            'source': 'Contact Form'
        })
        
        # Create support ticket/inquiry in ODOO
        odoo_ticket_id = None
        if odoo_contact_id:
            # For now, log as a potential ticket - full helpdesk integration can be added
            logger.info(f"Contact form inquiry from {form_data['name']} - Subject: {form_data['subject']}")
        
        # Update local record with ODOO IDs
        await db.contact_form_submissions.update_one(
            {"form_id": form_id},
            {
                "$set": {
                    "odoo_contact_id": odoo_contact_id,
                    "odoo_ticket_id": odoo_ticket_id,
                    "status": "processed" if odoo_contact_id else "odoo_error"
                }
            }
        )
        
        logger.info(f"ODOO integration completed for form {form_id}")
        
    except Exception as e:
        logger.error(f"ODOO integration failed for form {form_id}: {str(e)}")
        await db.contact_form_submissions.update_one(
            {"form_id": form_id},
            {"$set": {"status": "odoo_error"}}
        )

# Admin Contact Form Management Endpoints
@router.get("/admin/contact-forms")
async def get_contact_form_submissions(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all contact form submissions for admin review"""
    
    query = {}
    if status:
        query["status"] = status
    
    submissions = await db.contact_form_submissions.find(query).sort("submitted_at", -1).skip(offset).limit(limit).to_list(length=limit)
    total_count = await db.contact_form_submissions.count_documents(query)
    
    # Remove MongoDB ObjectIds
    for submission in submissions:
        if "_id" in submission:
            del submission["_id"]
    
    # Get statistics
    stats = {
        "total_submissions": await db.contact_form_submissions.count_documents({}),
        "pending_responses": await db.contact_form_submissions.count_documents({"admin_response": None}),
        "odoo_integrated": await db.contact_form_submissions.count_documents({"odoo_contact_id": {"$ne": None}}),
        "today_submissions": await db.contact_form_submissions.count_documents({
            "submitted_at": {"$gte": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)}
        })
    }
    
    return {
        "submissions": submissions,
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "statistics": stats
    }

@router.get("/admin/contact-forms/{form_id}")
async def get_contact_form_details(
    form_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get detailed information about a specific contact form submission"""
    
    submission = await db.contact_form_submissions.find_one({"form_id": form_id})
    if not submission:
        raise HTTPException(status_code=404, detail="Contact form submission not found")
    
    # Remove MongoDB ObjectId
    del submission["_id"]
    
    return {"submission": submission}

@router.post("/admin/contact-forms/{form_id}/respond")
async def respond_to_contact_form(
    form_id: str,
    response_data: AdminResponse,
    background_tasks: BackgroundTasks,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Admin response to contact form submission"""
    
    submission = await db.contact_form_submissions.find_one({"form_id": form_id})
    if not submission:
        raise HTTPException(status_code=404, detail="Contact form submission not found")
    
    # Update submission with admin response
    await db.contact_form_submissions.update_one(
        {"form_id": form_id},
        {
            "$set": {
                "admin_response": response_data.message,
                "admin_response_at": datetime.utcnow(),
                "admin_responder": current_user.email,
                "status": "responded"
            }
        }
    )
    
    # Send email response to customer
    background_tasks.add_task(
        send_contact_form_response_email,
        submission["email"],
        submission["name"],
        submission["subject"],
        response_data.message
    )
    
    return {
        "status": "success",
        "message": "Response sent successfully",
        "form_id": form_id
    }

async def send_contact_form_response_email(customer_email: str, customer_name: str, 
                                         original_subject: str, admin_response: str):
    """Send email response to customer"""
    try:
        # For now, log the email that would be sent
        # In production, integrate with actual email service (ODOO or other)
        email_log = {
            "to": customer_email,
            "subject": f"Re: {original_subject}",
            "body": f"""Dear {customer_name},

Thank you for contacting CustomerMind IQ. Here's our response to your inquiry:

{admin_response}

If you have any further questions, please don't hesitate to reach out.

Best regards,
CustomerMind IQ Support Team""",
            "sent_at": datetime.utcnow(),
            "type": "contact_form_response"
        }
        
        await db.email_logs.insert_one(email_log)
        logger.info(f"Contact form response email logged for {customer_email}")
        
        # Try to send via ODOO if available
        try:
            odoo_integration.send_email(
                customer_email,
                f"Re: {original_subject}",
                email_log["body"]
            )
        except Exception as odoo_error:
            logger.warning(f"ODOO email send failed, logged instead: {str(odoo_error)}")
        
    except Exception as e:
        logger.error(f"Failed to send contact form response email: {str(e)}")

# Contact Form Statistics for Admin Dashboard
@router.get("/admin/contact-forms/stats")
async def get_contact_form_statistics(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get contact form statistics for admin dashboard"""
    
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Aggregate statistics
    pipeline = [
        {"$match": {"submitted_at": {"$gte": date_from}}},
        {"$group": {
            "_id": {
                "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$submitted_at"
                }
            },
            "count": {"$sum": 1},
            "responded": {
                "$sum": {
                    "$cond": [{"$ne": ["$admin_response", None]}, 1, 0]
                }
            }
        }},
        {"$sort": {"_id": 1}}
    ]
    
    daily_stats = await db.contact_form_submissions.aggregate(pipeline).to_list(length=days)
    
    # Overall statistics
    total_forms = await db.contact_form_submissions.count_documents({"submitted_at": {"$gte": date_from}})
    responded_forms = await db.contact_form_submissions.count_documents({
        "submitted_at": {"$gte": date_from},
        "admin_response": {"$ne": None}
    })
    
    response_rate = (responded_forms / total_forms * 100) if total_forms > 0 else 0
    
    return {
        "period_days": days,
        "daily_statistics": daily_stats,
        "summary": {
            "total_submissions": total_forms,
            "responded_submissions": responded_forms,
            "pending_responses": total_forms - responded_forms,
            "response_rate_percent": round(response_rate, 2)
        }
    }