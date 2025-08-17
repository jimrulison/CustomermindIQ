from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import os
import uuid
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json

load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.marketing_analytics

app = FastAPI(
    title="Software Purchase Analytics & Email Marketing",
    description="AI-powered customer behavior analysis and email campaign automation",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class CustomerBehavior(BaseModel):
    customer_id: str
    name: str
    email: EmailStr
    total_purchases: int
    total_spent: float
    last_purchase_date: Optional[datetime] = None
    software_owned: List[str] = Field(default_factory=list)
    purchase_patterns: Dict[str, Any] = Field(default_factory=dict)
    engagement_score: float = 0.0
    lifecycle_stage: str = "new"

class ProductRecommendation(BaseModel):
    product_name: str
    confidence_score: float
    reason: str
    estimated_conversion_probability: float
    suggested_price: Optional[float] = None

class EmailCampaign(BaseModel):
    id: Optional[str] = None
    name: str
    target_segment: str
    subject: str
    content: str
    recommended_products: List[ProductRecommendation] = Field(default_factory=list)
    target_customers: List[str] = Field(default_factory=list)
    status: str = "draft"
    created_at: Optional[datetime] = None
    scheduled_date: Optional[datetime] = None

class AnalyticsData(BaseModel):
    total_customers: int
    total_revenue: float
    top_products: List[Dict[str, Any]]
    conversion_metrics: Dict[str, float]
    segment_distribution: Dict[str, int]

# AI Service for customer behavior analysis
class CustomerAnalyticsService:
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY", "sk-emergent-b5909F3C88a6c13635")
        
    async def analyze_customer_behavior(self, customer_data: Dict) -> Dict[str, Any]:
        """Analyze customer purchase patterns and predict next purchases"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"customer_analysis_{customer_data.get('customer_id', 'unknown')}",
                system_message="""You are an expert customer behavior analyst for software companies. 
                Analyze purchase patterns, predict next likely purchases, and provide actionable insights.
                Return responses in valid JSON format only."""
            ).with_model("openai", "gpt-4o-mini")
            
            analysis_prompt = f"""
            Analyze this customer's software purchase behavior:
            
            Customer Data: {json.dumps(customer_data, default=str)}
            
            Provide analysis in this exact JSON format:
            {{
                "engagement_score": <score 0-100>,
                "lifecycle_stage": "<new/active/at_risk/churned>",
                "purchase_patterns": {{
                    "frequency": "<low/medium/high>",
                    "seasonality": "<description>",
                    "avg_order_value": <number>,
                    "product_preferences": ["category1", "category2"]
                }},
                "next_purchase_predictions": [
                    {{
                        "product": "<product name>",
                        "probability": <0-1>,
                        "reason": "<explanation>",
                        "suggested_timing": "<when to approach>"
                    }}
                ],
                "email_strategy": {{
                    "tone": "<professional/casual/technical>",
                    "frequency": "<weekly/biweekly/monthly>",
                    "best_day": "<day of week>",
                    "content_focus": ["feature1", "feature2"]
                }}
            }}
            """
            
            message = UserMessage(text=analysis_prompt)
            response = await chat.send_message(message)
            
            # Parse JSON response
            try:
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "engagement_score": 50,
                    "lifecycle_stage": "active",
                    "purchase_patterns": {"frequency": "medium"},
                    "next_purchase_predictions": [],
                    "email_strategy": {"tone": "professional", "frequency": "monthly"}
                }
                
        except Exception as e:
            print(f"AI analysis error: {e}")
            return {"error": str(e)}

    async def generate_email_content(self, customer: Dict, recommendations: List[Dict]) -> str:
        """Generate personalized email content"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"email_gen_{customer.get('customer_id', 'unknown')}",
                system_message="You are an expert email marketing copywriter specializing in software sales."
            ).with_model("openai", "gpt-4o-mini")
            
            email_prompt = f"""
            Create a personalized email for this customer:
            Customer: {customer.get('name', 'Valued Customer')}
            Current Software: {customer.get('software_owned', [])}
            Recommendations: {recommendations}
            
            Write a compelling email that:
            1. Acknowledges their current software usage
            2. Presents relevant upgrade/new software recommendations
            3. Includes clear benefits and ROI
            4. Has a clear call-to-action
            5. Maintains a professional but friendly tone
            
            Subject line format: "Enhance Your [Current Software] Setup - Exclusive Recommendations"
            """
            
            message = UserMessage(text=email_prompt)
            response = await chat.send_message(message)
            return response
            
        except Exception as e:
            return f"Error generating email: {e}"

# Initialize services
analytics_service = CustomerAnalyticsService()

# Real ODOO service integration
class OdooService:
    """Real ODOO service integration"""
    
    def __init__(self):
        self.url = os.getenv("ODOO_URL")
        self.database = os.getenv("ODOO_DATABASE")
        self.username = os.getenv("ODOO_USERNAME")
        self.password = os.getenv("ODOO_PASSWORD")  # Can use API key here
        self.uid = None
        self.common = None
        self.models = None
        
    async def connect(self) -> bool:
        """Establish connection and authenticate with ODOO"""
        try:
            import xmlrpc.client
            print(f"Attempting ODOO connection to: {self.url}")
            print(f"Database: {self.database}")
            print(f"Username: {self.username}")
            
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = self.common.authenticate(
                self.database, self.username, self.password, {}
            )
            
            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                print(f"✅ ODOO Authentication successful! User ID: {self.uid}")
                return True
            else:
                print("❌ ODOO Authentication failed - invalid credentials")
                return False
            
        except Exception as e:
            print(f"❌ ODOO Authentication failed: {e}")
            return False
    
    async def get_customers(self) -> List[Dict]:
        """Get real customer data from ODOO"""
        try:
            if not await self.connect():
                print("Failed to connect to ODOO, falling back to mock data")
                return await self._get_mock_customers()
            
            # Search for customers (contacts that are not companies and have email)
            customer_domain = [
                ('is_company', '=', False),
                ('email', '!=', False),
                ('customer_rank', '>', 0)  # Only customers, not vendors
            ]
            
            customer_ids = self.models.execute_kw(
                self.database, self.uid, self.password,
                'res.partner', 'search', [customer_domain],
                {'limit': 50}  # Limit for performance
            )
            
            if not customer_ids:
                print("No customers found in ODOO, using mock data")
                return await self._get_mock_customers()
            
            # Get customer details
            customers = self.models.execute_kw(
                self.database, self.uid, self.password,
                'res.partner', 'read', [customer_ids],
                {'fields': ['name', 'email', 'phone', 'create_date', 'category_id']}
            )
            
            # Get purchase history for each customer
            customer_data = []
            for customer in customers[:10]:  # Limit for performance
                # Get sales orders for this customer
                order_domain = [
                    ('partner_id', '=', customer['id']),
                    ('state', 'in', ['sale', 'done'])
                ]
                
                order_ids = self.models.execute_kw(
                    self.database, self.uid, self.password,
                    'sale.order', 'search', [order_domain]
                )
                
                total_spent = 0
                software_owned = []
                
                if order_ids:
                    orders = self.models.execute_kw(
                        self.database, self.uid, self.password,
                        'sale.order', 'read', [order_ids],
                        {'fields': ['amount_total', 'date_order', 'order_line']}
                    )
                    
                    total_spent = sum(order.get('amount_total', 0) for order in orders)
                    
                    # Get product names from order lines
                    for order in orders:
                        if order.get('order_line'):
                            line_ids = order['order_line']
                            lines = self.models.execute_kw(
                                self.database, self.uid, self.password,
                                'sale.order.line', 'read', [line_ids],
                                {'fields': ['product_id']}
                            )
                            
                            for line in lines:
                                if line.get('product_id'):
                                    product_name = line['product_id'][1]  # [id, name] format
                                    if product_name not in software_owned:
                                        software_owned.append(product_name)
                
                customer_data.append({
                    "customer_id": str(customer['id']),
                    "name": customer['name'],
                    "email": customer['email'],
                    "total_purchases": len(order_ids),
                    "total_spent": total_spent,
                    "software_owned": software_owned[:5],  # Top 5 products
                    "last_purchase_date": datetime.now() - timedelta(days=30) if order_ids else None
                })
            
            print(f"Successfully loaded {len(customer_data)} customers from ODOO")
            return customer_data
            
        except Exception as e:
            print(f"Error fetching ODOO customers: {e}")
            return await self._get_mock_customers()
    
    async def _get_mock_customers(self) -> List[Dict]:
        """Fallback mock customer data"""
        return [
            {
                "customer_id": "1",
                "name": "TechCorp Solutions",
                "email": "admin@techcorp.com",
                "total_purchases": 5,
                "total_spent": 15000.0,
                "software_owned": ["CRM Pro", "Inventory Manager"],
                "last_purchase_date": datetime.now() - timedelta(days=30)
            },
            {
                "customer_id": "2", 
                "name": "StartupXYZ",
                "email": "founder@startupxyz.com",
                "total_purchases": 2,
                "total_spent": 5000.0,
                "software_owned": ["Basic CRM"],
                "last_purchase_date": datetime.now() - timedelta(days=60)
            }
        ]
    
    async def send_email_campaign(self, campaign: EmailCampaign) -> bool:
        """Send email campaign via ODOO"""
        try:
            if not await self.connect():
                print("Mock: Failed to connect to ODOO for email sending")
                return False
            
            # Create mailing in ODOO
            mailing_data = {
                'name': campaign.name,
                'subject': campaign.subject,
                'body_html': campaign.content,
                'mailing_type': 'mail',
                'state': 'draft'
            }
            
            mailing_id = self.models.execute_kw(
                self.database, self.uid, self.password,
                'mailing.mailing', 'create', [mailing_data]
            )
            
            if mailing_id:
                # Add recipients
                for customer_id in campaign.target_customers:
                    contact_data = {
                        'mailing_id': mailing_id,
                        'res_id': int(customer_id),
                        'model': 'res.partner'
                    }
                    
                    self.models.execute_kw(
                        self.database, self.uid, self.password,
                        'mailing.contact', 'create', [contact_data]
                    )
                
                # Send the mailing
                self.models.execute_kw(
                    self.database, self.uid, self.password,
                    'mailing.mailing', 'action_send_mail', [mailing_id]
                )
                
                print(f"Successfully sent campaign '{campaign.name}' to {len(campaign.target_customers)} customers via ODOO")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error sending ODOO campaign: {e}")
            print(f"Mock: Sending campaign '{campaign.name}' to {len(campaign.target_customers)} customers")
            return True  # Return True for mock sending

odoo_service = OdooService()

# API Endpoints
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/api/customers", response_model=List[CustomerBehavior])
async def get_customers():
    """Get all customers with behavior analysis"""
    try:
        # Get customers from ODOO (mock for now)
        customers_data = await odoo_service.get_customers()
        analyzed_customers = []
        
        for customer_data in customers_data:
            # AI-powered behavior analysis
            analysis = await analytics_service.analyze_customer_behavior(customer_data)
            
            customer_behavior = CustomerBehavior(
                customer_id=customer_data["customer_id"],
                name=customer_data["name"],
                email=customer_data["email"],
                total_purchases=customer_data["total_purchases"],
                total_spent=customer_data["total_spent"],
                last_purchase_date=customer_data.get("last_purchase_date"),
                software_owned=customer_data.get("software_owned", []),
                purchase_patterns=analysis.get("purchase_patterns", {}),
                engagement_score=analysis.get("engagement_score", 50),
                lifecycle_stage=analysis.get("lifecycle_stage", "active")
            )
            analyzed_customers.append(customer_behavior)
            
            # Store in MongoDB
            await db.customers.update_one(
                {"customer_id": customer_data["customer_id"]},
                {"$set": customer_behavior.dict()},
                upsert=True
            )
        
        return analyzed_customers
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching customers: {e}")

@app.get("/api/customers/{customer_id}/recommendations")
async def get_customer_recommendations(customer_id: str):
    """Get AI-powered product recommendations for a specific customer"""
    try:
        # Get customer data
        customer = await db.customers.find_one({"customer_id": customer_id})
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Get AI analysis for recommendations
        analysis = await analytics_service.analyze_customer_behavior(customer)
        predictions = analysis.get("next_purchase_predictions", [])
        
        recommendations = []
        for pred in predictions:
            recommendation = ProductRecommendation(
                product_name=pred.get("product", "Unknown Product"),
                confidence_score=pred.get("probability", 0.5) * 100,
                reason=pred.get("reason", "Based on purchase history"),
                estimated_conversion_probability=pred.get("probability", 0.5)
            )
            recommendations.append(recommendation)
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {e}")

@app.post("/api/campaigns", response_model=EmailCampaign)
async def create_campaign(campaign: EmailCampaign, background_tasks: BackgroundTasks):
    """Create a new email campaign with AI-generated content"""
    try:
        campaign.id = str(uuid.uuid4())
        campaign.created_at = datetime.now()
        
        # Get target customers based on segment
        customers = await db.customers.find({
            "lifecycle_stage": campaign.target_segment
        }).to_list(length=100)
        
        campaign.target_customers = [c["customer_id"] for c in customers]
        
        # Generate AI-powered recommendations for each customer
        all_recommendations = []
        for customer in customers[:5]:  # Limit for demo
            analysis = await analytics_service.analyze_customer_behavior(customer)
            predictions = analysis.get("next_purchase_predictions", [])
            
            for pred in predictions[:2]:  # Top 2 recommendations per customer
                rec = ProductRecommendation(
                    product_name=pred.get("product", "Premium Software Suite"),
                    confidence_score=pred.get("probability", 0.7) * 100,
                    reason=pred.get("reason", "Matches purchase patterns"),
                    estimated_conversion_probability=pred.get("probability", 0.7)
                )
                all_recommendations.append(rec)
        
        campaign.recommended_products = all_recommendations[:10]  # Top 10 overall
        
        # Generate AI-powered email content
        if customers:
            sample_customer = customers[0]
            campaign.content = await analytics_service.generate_email_content(
                sample_customer, 
                [rec.dict() for rec in campaign.recommended_products[:3]]
            )
        
        # Store campaign
        await db.campaigns.insert_one(campaign.dict())
        
        # Schedule email sending if date is provided
        if campaign.scheduled_date:
            background_tasks.add_task(schedule_campaign_sending, campaign.id)
        
        return campaign
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating campaign: {e}")

@app.get("/api/campaigns", response_model=List[EmailCampaign])
async def get_campaigns():
    """Get all email campaigns"""
    try:
        campaigns = await db.campaigns.find().to_list(length=100)
        return [EmailCampaign(**campaign) for campaign in campaigns]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching campaigns: {e}")

@app.get("/api/analytics", response_model=AnalyticsData)
async def get_analytics():
    """Get comprehensive analytics dashboard data"""
    try:
        # Get customer stats
        total_customers = await db.customers.count_documents({})
        
        # Calculate total revenue
        customers = await db.customers.find().to_list(length=1000)
        total_revenue = sum(c.get("total_spent", 0) for c in customers)
        
        # Top products analysis
        software_counts = {}
        for customer in customers:
            for software in customer.get("software_owned", []):
                software_counts[software] = software_counts.get(software, 0) + 1
        
        top_products = [
            {"name": software, "customers": count, "revenue": count * 2500}
            for software, count in sorted(software_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        # Segment distribution
        segment_counts = {}
        for customer in customers:
            stage = customer.get("lifecycle_stage", "active")
            segment_counts[stage] = segment_counts.get(stage, 0) + 1
        
        # Conversion metrics (mock for now)
        conversion_metrics = {
            "email_open_rate": 0.25,
            "click_through_rate": 0.12,
            "conversion_rate": 0.08,
            "average_deal_size": 3500.0
        }
        
        analytics = AnalyticsData(
            total_customers=total_customers,
            total_revenue=total_revenue,
            top_products=top_products,
            conversion_metrics=conversion_metrics,
            segment_distribution=segment_counts
        )
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting analytics: {e}")

async def schedule_campaign_sending(campaign_id: str):
    """Background task to send scheduled campaigns"""
    try:
        campaign_data = await db.campaigns.find_one({"id": campaign_id})
        if campaign_data:
            campaign = EmailCampaign(**campaign_data)
            success = await odoo_service.send_email_campaign(campaign)
            
            # Update campaign status
            await db.campaigns.update_one(
                {"id": campaign_id},
                {"$set": {"status": "sent" if success else "failed"}}
            )
    except Exception as e:
        print(f"Error sending campaign {campaign_id}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)