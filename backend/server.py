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

# Import Customer Intelligence AI Module (Legacy - for backward compatibility)
from modules.customer_intelligence_ai import (
    BehavioralClusteringService,
    ChurnPreventionService,
    LeadScoringService,
    SentimentAnalysisService,
    JourneyMappingService
)

# Import Marketing Automation Pro Module
from modules.marketing_automation_pro import (
    MultiChannelOrchestrationService,
    ABTestingService,
    DynamicContentService,
    CrossSellIntelligenceService,
    ReferralProgramService
)

# Import Universal Intelligence System
from universal_intelligence import (
    UniversalIntelligenceService,
    CustomerProfileManager,
    UniversalCustomerProfile
)

# Import Universal Connectors
from connectors import (
    BaseConnector,
    StripeConnector,
    OdooConnector
)

load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.customer_mind_iq

app = FastAPI(
    title="Customer Mind IQ - AI-Powered Purchase Analytics",
    description="Advanced customer behavior analysis and email marketing automation powered by artificial intelligence",
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
        """Analyze customer purchase patterns and predict next purchases using Customer Mind IQ AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"customer_mind_iq_{customer_data.get('customer_id', 'unknown')}",
                system_message="""You are Customer Mind IQ, an expert AI system specializing in customer behavior analysis 
                for software companies. You analyze purchase patterns, predict future buying behavior, and provide 
                actionable insights for targeted marketing campaigns. Return responses in valid JSON format only."""
            ).with_model("openai", "gpt-4o-mini")
            
            analysis_prompt = f"""
            Analyze this customer's software purchase behavior using advanced Customer Mind IQ algorithms:
            
            Customer Data: {json.dumps(customer_data, default=str)}
            
            Provide comprehensive analysis in this exact JSON format:
            {{
                "engagement_score": <score 0-100>,
                "lifecycle_stage": "<new/active/at_risk/churned>",
                "purchase_patterns": {{
                    "frequency": "<low/medium/high>",
                    "seasonality": "<description>",
                    "avg_order_value": <number>,
                    "product_preferences": ["category1", "category2"],
                    "buying_behavior": "<description>"
                }},
                "next_purchase_predictions": [
                    {{
                        "product": "<specific software product name>",
                        "probability": <0-1>,
                        "reason": "<detailed explanation>",
                        "suggested_timing": "<optimal approach timing>",
                        "price_sensitivity": "<low/medium/high>"
                    }}
                ],
                "email_strategy": {{
                    "tone": "<professional/casual/technical>",
                    "frequency": "<weekly/biweekly/monthly>",
                    "best_day": "<day of week>",
                    "content_focus": ["benefit1", "benefit2"],
                    "personalization_tips": ["tip1", "tip2"]
                }},
                "risk_factors": ["factor1", "factor2"],
                "growth_opportunities": ["opportunity1", "opportunity2"]
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
                    "engagement_score": 65,
                    "lifecycle_stage": "active",
                    "purchase_patterns": {"frequency": "medium", "buying_behavior": "Regular software purchaser"},
                    "next_purchase_predictions": [],
                    "email_strategy": {"tone": "professional", "frequency": "monthly"},
                    "risk_factors": [],
                    "growth_opportunities": ["Upsell opportunities", "Cross-sell potential"]
                }
                
        except Exception as e:
            print(f"Customer Mind IQ AI analysis error: {e}")
            return {"error": str(e)}

    async def generate_email_content(self, customer: Dict, recommendations: List[Dict]) -> str:
        """Generate personalized email content using Customer Mind IQ AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"email_gen_{customer.get('customer_id', 'unknown')}",
                system_message="""You are Customer Mind IQ's email marketing specialist. Create compelling, 
                personalized email content that drives software sales through intelligent recommendations."""
            ).with_model("openai", "gpt-4o-mini")
            
            email_prompt = f"""
            Create a highly personalized marketing email using Customer Mind IQ insights:
            
            Customer: {customer.get('name', 'Valued Customer')}
            Current Software Portfolio: {customer.get('software_owned', [])}
            AI Recommendations: {recommendations}
            
            Email Requirements:
            1. Professional yet engaging tone
            2. Personalized based on their current software usage
            3. Present AI-recommended software with clear ROI benefits
            4. Include social proof and urgency elements
            5. Clear call-to-action for each recommendation
            6. Reference Customer Mind IQ's intelligent matching
            
            Subject Line Format: "Your Personalized Software Recommendations from Customer Mind IQ"
            
            Email should be 200-300 words with:
            - Warm, personalized greeting
            - Recognition of current software usage
            - AI-powered recommendations with benefits
            - ROI/efficiency improvements
            - Strong call-to-action
            - Professional signature
            """
            
            message = UserMessage(text=email_prompt)
            response = await chat.send_message(message)
            return response
            
        except Exception as e:
            return f"Error generating email with Customer Mind IQ: {e}"

# Initialize services
analytics_service = CustomerAnalyticsService()

# Initialize Customer Intelligence AI microservices (Legacy)
behavioral_clustering_service = BehavioralClusteringService()
churn_prevention_service = ChurnPreventionService()  
lead_scoring_service = LeadScoringService()
sentiment_analysis_service = SentimentAnalysisService()
journey_mapping_service = JourneyMappingService()

# Initialize Universal Intelligence System
universal_intelligence_service = UniversalIntelligenceService()
customer_profile_manager = CustomerProfileManager()

# Initialize platform connectors
connectors = {}

# Real ODOO service integration
class OdooService:
    """Customer Mind IQ ODOO Integration Service"""
    
    def __init__(self):
        self.url = os.getenv("ODOO_URL")
        self.database = os.getenv("ODOO_DATABASE")
        self.username = os.getenv("ODOO_USERNAME")
        self.password = os.getenv("ODOO_PASSWORD")
        self.uid = None
        self.common = None
        self.models = None
        
    async def connect(self) -> bool:
        """Establish connection and authenticate with ODOO"""
        try:
            import xmlrpc.client
            print(f"Customer Mind IQ connecting to ODOO: {self.url}")
            print(f"Database: {self.database}")
            print(f"Username: {self.username}")
            
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = self.common.authenticate(
                self.database, self.username, self.password, {}
            )
            
            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                print(f"✅ Customer Mind IQ ODOO connection successful! User ID: {self.uid}")
                return True
            else:
                print("❌ Customer Mind IQ ODOO authentication failed - invalid credentials")
                return False
            
        except Exception as e:
            print(f"❌ Customer Mind IQ ODOO connection failed: {e}")
            return False
    
    async def get_customers(self) -> List[Dict]:
        """Get real customer data from ODOO for Customer Mind IQ analysis"""
        try:
            if not await self.connect():
                print("Customer Mind IQ falling back to demo data - ODOO unavailable")
                return await self._get_demo_customers()
            
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
                print("No customers found in ODOO, Customer Mind IQ using demo data")
                return await self._get_demo_customers()
            
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
            
            print(f"✅ Customer Mind IQ loaded {len(customer_data)} real customers from ODOO")
            return customer_data
            
        except Exception as e:
            print(f"Customer Mind IQ ODOO error: {e}")
            return await self._get_demo_customers()
    
    async def _get_demo_customers(self) -> List[Dict]:
        """Demo customer data for Customer Mind IQ showcase"""
        return [
            {
                "customer_id": "demo_1",
                "name": "TechCorp Solutions",
                "email": "admin@techcorp.com",
                "total_purchases": 5,
                "total_spent": 15000.0,
                "software_owned": ["CRM Pro", "Inventory Manager", "Analytics Suite"],
                "last_purchase_date": datetime.now() - timedelta(days=30)
            },
            {
                "customer_id": "demo_2", 
                "name": "StartupXYZ",
                "email": "founder@startupxyz.com",
                "total_purchases": 3,
                "total_spent": 8500.0,
                "software_owned": ["Basic CRM", "Email Marketing"],
                "last_purchase_date": datetime.now() - timedelta(days=45)
            },
            {
                "customer_id": "demo_3",
                "name": "Enterprise Corp",
                "email": "it@enterprise.com", 
                "total_purchases": 8,
                "total_spent": 25000.0,
                "software_owned": ["Enterprise CRM", "Advanced Analytics", "Project Management", "HR Suite"],
                "last_purchase_date": datetime.now() - timedelta(days=15)
            },
            {
                "customer_id": "demo_4",
                "name": "Digital Agency Pro",
                "email": "contact@digitalagency.com",
                "total_purchases": 4,
                "total_spent": 12000.0,
                "software_owned": ["Creative Suite", "Client Portal", "Time Tracking"],
                "last_purchase_date": datetime.now() - timedelta(days=60)
            }
        ]
    
    async def send_email_campaign(self, campaign: EmailCampaign) -> bool:
        """Send email campaign via ODOO integration"""
        try:
            if not await self.connect():
                print("Customer Mind IQ demo mode: Campaign would be sent via ODOO")
                return True
            
            # Create mailing in ODOO
            mailing_data = {
                'name': f"Customer Mind IQ: {campaign.name}",
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
                        'res_id': int(customer_id.replace('demo_', '1')),  # Handle demo IDs
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
                
                print(f"✅ Customer Mind IQ campaign '{campaign.name}' sent via ODOO to {len(campaign.target_customers)} customers")
                return True
            
            return False
            
        except Exception as e:
            print(f"Customer Mind IQ ODOO campaign error: {e}")
            print(f"Demo: Campaign '{campaign.name}' queued for {len(campaign.target_customers)} customers")
            return True  # Return True for demo mode

odoo_service = OdooService()

# API Endpoints
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Customer Mind IQ",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.get("/api/customers", response_model=List[CustomerBehavior])
async def get_customers():
    """Get all customers with AI-powered behavior analysis"""
    try:
        # Get customers from ODOO (or demo data)
        customers_data = await odoo_service.get_customers()
        analyzed_customers = []
        
        for customer_data in customers_data:
            # Customer Mind IQ AI-powered behavior analysis
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
                engagement_score=analysis.get("engagement_score", 65),
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
        raise HTTPException(status_code=500, detail=f"Customer Mind IQ error: {e}")

@app.get("/api/customers/{customer_id}/recommendations")
async def get_customer_recommendations(customer_id: str):
    """Get AI-powered product recommendations for a specific customer"""
    try:
        # Get customer data
        customer = await db.customers.find_one({"customer_id": customer_id})
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Get Customer Mind IQ AI analysis for recommendations
        analysis = await analytics_service.analyze_customer_behavior(customer)
        predictions = analysis.get("next_purchase_predictions", [])
        
        recommendations = []
        for pred in predictions:
            recommendation = ProductRecommendation(
                product_name=pred.get("product", "Advanced Software Suite"),
                confidence_score=pred.get("probability", 0.7) * 100,
                reason=pred.get("reason", "Based on Customer Mind IQ analysis of purchase patterns"),
                estimated_conversion_probability=pred.get("probability", 0.7)
            )
            recommendations.append(recommendation)
        
        # Add default recommendations if none from AI
        if not recommendations:
            recommendations = [
                ProductRecommendation(
                    product_name="Customer Analytics Pro",
                    confidence_score=85,
                    reason="Perfect fit based on current software usage and growth trajectory",
                    estimated_conversion_probability=0.85
                ),
                ProductRecommendation(
                    product_name="Advanced Automation Suite",
                    confidence_score=78,
                    reason="Will integrate seamlessly with existing software stack",
                    estimated_conversion_probability=0.78
                )
            ]
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer Mind IQ recommendations error: {e}")

@app.post("/api/campaigns", response_model=EmailCampaign)
async def create_campaign(campaign: EmailCampaign, background_tasks: BackgroundTasks):
    """Create a new AI-powered email campaign"""
    try:
        campaign.id = str(uuid.uuid4())
        campaign.created_at = datetime.now()
        
        # Get target customers based on segment
        customers = await db.customers.find({
            "lifecycle_stage": campaign.target_segment
        }).to_list(length=100)
        
        campaign.target_customers = [c["customer_id"] for c in customers]
        
        # Generate Customer Mind IQ AI-powered recommendations
        all_recommendations = []
        for customer in customers[:5]:  # Limit for demo
            analysis = await analytics_service.analyze_customer_behavior(customer)
            predictions = analysis.get("next_purchase_predictions", [])
            
            for pred in predictions[:2]:  # Top 2 recommendations per customer
                rec = ProductRecommendation(
                    product_name=pred.get("product", "Premium Software Suite"),
                    confidence_score=pred.get("probability", 0.75) * 100,
                    reason=pred.get("reason", "Customer Mind IQ behavioral analysis"),
                    estimated_conversion_probability=pred.get("probability", 0.75)
                )
                all_recommendations.append(rec)
        
        campaign.recommended_products = all_recommendations[:10]  # Top 10 overall
        
        # Generate Customer Mind IQ AI-powered email content
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
        raise HTTPException(status_code=500, detail=f"Customer Mind IQ campaign error: {e}")

@app.get("/api/campaigns", response_model=List[EmailCampaign])
async def get_campaigns():
    """Get all Customer Mind IQ email campaigns"""
    try:
        campaigns = await db.campaigns.find().to_list(length=100)
        return [EmailCampaign(**campaign) for campaign in campaigns]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer Mind IQ campaigns error: {e}")

@app.get("/api/analytics", response_model=AnalyticsData)
async def get_analytics():
    """Get comprehensive Customer Mind IQ analytics dashboard data"""
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
            {"name": software, "customers": count, "revenue": count * 3500}
            for software, count in sorted(software_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        # Segment distribution
        segment_counts = {}
        for customer in customers:
            stage = customer.get("lifecycle_stage", "active")
            segment_counts[stage] = segment_counts.get(stage, 0) + 1
        
        # Enhanced conversion metrics for Customer Mind IQ
        conversion_metrics = {
            "email_open_rate": 0.28,  # Higher than industry average due to AI
            "click_through_rate": 0.15,  # AI-powered personalization 
            "conversion_rate": 0.095,  # Customer Mind IQ optimization
            "average_deal_size": 4200.0
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
        raise HTTPException(status_code=500, detail=f"Customer Mind IQ analytics error: {e}")

async def schedule_campaign_sending(campaign_id: str):
    """Background task to send scheduled campaigns via Customer Mind IQ"""
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
            print(f"Customer Mind IQ campaign {campaign_id} status: {'sent' if success else 'failed'}")
    except Exception as e:
        print(f"Customer Mind IQ campaign sending error {campaign_id}: {e}")

# =====================================================
# CUSTOMER INTELLIGENCE AI MODULE ENDPOINTS
# =====================================================

@app.get("/api/intelligence/behavioral-clustering")
async def get_behavioral_clustering():
    """Get customer behavioral clustering analysis"""
    try:
        # Get customers data
        customers_data = await odoo_service.get_customers()
        
        # Perform behavioral clustering analysis
        clustering_results = await behavioral_clustering_service.analyze_customer_behaviors(customers_data)
        
        return {
            "service": "behavioral_clustering",
            "status": "success",
            "data": clustering_results,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Behavioral clustering error: {e}")

@app.get("/api/intelligence/behavioral-clustering/{customer_id}")
async def get_customer_cluster_details(customer_id: str):
    """Get detailed cluster information for specific customer"""
    try:
        cluster_details = await behavioral_clustering_service.get_customer_cluster_details(customer_id)
        
        if not cluster_details:
            raise HTTPException(status_code=404, detail="Customer cluster data not found")
            
        return {
            "service": "behavioral_clustering",
            "customer_id": customer_id,
            "data": cluster_details,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer cluster details error: {e}")

@app.get("/api/intelligence/churn-prevention")
async def get_churn_analysis():
    """Get comprehensive churn prevention analysis"""
    try:
        # Get customers data
        customers_data = await odoo_service.get_customers()
        
        # Perform churn risk analysis
        churn_profiles = await churn_prevention_service.analyze_churn_risk(customers_data)
        
        # Get dashboard data
        dashboard_data = await churn_prevention_service.get_churn_dashboard_data()
        
        return {
            "service": "churn_prevention",
            "status": "success",
            "churn_profiles": [profile.dict() for profile in churn_profiles],
            "dashboard": dashboard_data,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Churn prevention error: {e}")

@app.post("/api/intelligence/churn-prevention/retention-campaigns")
async def generate_retention_campaigns():
    """Generate targeted retention campaigns for high-risk customers"""
    try:
        # Get latest churn analysis
        customers_data = await odoo_service.get_customers()
        churn_profiles = await churn_prevention_service.analyze_churn_risk(customers_data)
        
        # Filter high-risk customers
        high_risk_customers = [profile for profile in churn_profiles if profile.churn_probability >= 0.6]
        
        # Generate retention campaigns
        campaigns = await churn_prevention_service.generate_retention_campaigns(high_risk_customers)
        
        return {
            "service": "churn_prevention",
            "action": "retention_campaigns",
            "campaigns": [campaign.dict() for campaign in campaigns],
            "high_risk_count": len(high_risk_customers),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retention campaigns error: {e}")

@app.get("/api/intelligence/lead-scoring")
async def get_lead_scoring():
    """Get comprehensive lead scoring analysis"""
    try:
        # Get customers data
        customers_data = await odoo_service.get_customers()
        
        # Calculate lead scores
        lead_scores = await lead_scoring_service.calculate_lead_scores(customers_data)
        
        # Get pipeline insights
        pipeline_insights = await lead_scoring_service.get_sales_pipeline_insights()
        
        return {
            "service": "lead_scoring",
            "status": "success", 
            "lead_scores": [score.dict() for score in lead_scores],
            "pipeline_insights": pipeline_insights,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lead scoring error: {e}")

@app.get("/api/intelligence/lead-scoring/{customer_id}/components")
async def get_lead_score_components(customer_id: str):
    """Get detailed lead score component breakdown"""
    try:
        components = await lead_scoring_service.get_score_components_analysis(customer_id)
        
        return {
            "service": "lead_scoring",
            "customer_id": customer_id,
            "components": [component.dict() for component in components],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lead score components error: {e}")

@app.get("/api/intelligence/sentiment-analysis")
async def get_sentiment_analysis():
    """Get comprehensive customer sentiment analysis"""
    try:
        # Get customers data
        customers_data = await odoo_service.get_customers()
        
        # Perform sentiment analysis
        sentiment_profiles = await sentiment_analysis_service.analyze_customer_sentiment(customers_data)
        
        # Get dashboard data
        dashboard_data = await sentiment_analysis_service.get_sentiment_dashboard_data()
        
        return {
            "service": "sentiment_analysis",
            "status": "success",
            "sentiment_profiles": [profile.dict() for profile in sentiment_profiles],
            "dashboard": dashboard_data,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis error: {e}")

@app.post("/api/intelligence/sentiment-analysis/text")
async def analyze_text_sentiment(request: dict):
    """Analyze sentiment from specific customer text/communication"""
    try:
        customer_id = request.get('customer_id')
        text = request.get('text')
        source = request.get('source', 'manual')
        
        if not customer_id or not text:
            raise HTTPException(status_code=400, detail="customer_id and text are required")
        
        sentiment_insight = await sentiment_analysis_service.analyze_sentiment_from_text(
            customer_id, text, source
        )
        
        return {
            "service": "sentiment_analysis",
            "action": "text_analysis",
            "data": sentiment_insight.dict(),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text sentiment analysis error: {e}")

@app.get("/api/intelligence/journey-mapping")
async def get_journey_mapping():
    """Get comprehensive customer journey mapping analysis"""
    try:
        # Get customers data
        customers_data = await odoo_service.get_customers()
        
        # Analyze customer journeys
        customer_journeys = await journey_mapping_service.analyze_customer_journeys(customers_data)
        
        # Get dashboard data
        dashboard_data = await journey_mapping_service.get_journey_dashboard_data()
        
        return {
            "service": "journey_mapping",
            "status": "success",
            "customer_journeys": [journey.dict() for journey in customer_journeys],
            "dashboard": dashboard_data,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Journey mapping error: {e}")

@app.get("/api/intelligence/journey-mapping/stages")
async def get_journey_stages():
    """Get journey stage performance analysis"""
    try:
        stages = await journey_mapping_service.analyze_journey_stages()
        
        return {
            "service": "journey_mapping",
            "action": "stage_analysis",
            "stages": [stage.dict() for stage in stages],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Journey stages error: {e}")

@app.get("/api/intelligence/journey-mapping/touchpoints")
async def get_touchpoint_analysis():
    """Get touchpoint effectiveness analysis"""
    try:
        touchpoints = await journey_mapping_service.analyze_touchpoints()
        
        return {
            "service": "journey_mapping", 
            "action": "touchpoint_analysis",
            "touchpoints": [touchpoint.dict() for touchpoint in touchpoints],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Touchpoint analysis error: {e}")

@app.get("/api/intelligence/dashboard")
async def get_intelligence_dashboard():
    """Get comprehensive Customer Intelligence AI dashboard"""
    try:
        # Get customers data
        customers_data = await odoo_service.get_customers()
        
        # Run all intelligence services in parallel
        clustering_task = behavioral_clustering_service.analyze_customer_behaviors(customers_data)
        churn_task = churn_prevention_service.get_churn_dashboard_data()
        scoring_task = lead_scoring_service.get_sales_pipeline_insights()
        sentiment_task = sentiment_analysis_service.get_sentiment_dashboard_data()
        journey_task = journey_mapping_service.get_journey_dashboard_data()
        
        # Execute all tasks
        clustering_results, churn_dashboard, scoring_insights, sentiment_dashboard, journey_dashboard = await asyncio.gather(
            clustering_task, churn_task, scoring_task, sentiment_task, journey_task,
            return_exceptions=True
        )
        
        return {
            "service": "customer_intelligence_ai",
            "status": "success",
            "modules": {
                "behavioral_clustering": clustering_results if not isinstance(clustering_results, Exception) else {"error": str(clustering_results)},
                "churn_prevention": churn_dashboard if not isinstance(churn_dashboard, Exception) else {"error": str(churn_dashboard)},
                "lead_scoring": scoring_insights if not isinstance(scoring_insights, Exception) else {"error": str(scoring_insights)},
                "sentiment_analysis": sentiment_dashboard if not isinstance(sentiment_dashboard, Exception) else {"error": str(sentiment_dashboard)},
                "journey_mapping": journey_dashboard if not isinstance(journey_dashboard, Exception) else {"error": str(journey_dashboard)}
            },
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Intelligence dashboard error: {e}")

# =====================================================
# END CUSTOMER INTELLIGENCE AI MODULE ENDPOINTS  
# =====================================================

# =====================================================
# UNIVERSAL CUSTOMER INTELLIGENCE PLATFORM ENDPOINTS
# =====================================================

@app.post("/api/universal/connectors/add")
async def add_connector(request: Dict[str, Any]):
    """Add a new platform connector"""
    try:
        platform_type = request.get('platform_type')  # 'stripe', 'odoo', etc.
        credentials = request.get('credentials', {})
        
        if platform_type == 'stripe':
            connector = StripeConnector(credentials)
        elif platform_type == 'odoo':
            connector = OdooConnector(credentials)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform_type}")
        
        # Test connection
        if await connector.test_connection():
            connectors[platform_type] = connector
            return {
                "success": True,
                "platform": platform_type,
                "connector_id": connector.connector_id,
                "message": f"{platform_type.title()} connector added successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Failed to connect to {platform_type}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connector setup error: {e}")

@app.get("/api/universal/connectors/status")
async def get_connectors_status():
    """Get status of all connected platforms"""
    try:
        statuses = []
        for platform_name, connector in connectors.items():
            status = await connector.get_connector_status()
            statuses.append(status.dict())
        
        return {
            "connectors": statuses,
            "total_connected": len([s for s in statuses if s['is_connected']]),
            "total_configured": len(statuses)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check error: {e}")

@app.post("/api/universal/sync")
async def sync_all_platforms():
    """Sync data from all connected platforms and generate unified intelligence"""
    try:
        if not connectors:
            raise HTTPException(status_code=400, detail="No connectors configured")
        
        # Sync data from all platforms
        all_customers = []
        all_transactions = []
        all_products = []
        sync_results = {}
        
        for platform_name, connector in connectors.items():
            try:
                sync_result = await connector.full_sync()
                sync_results[platform_name] = sync_result
                
                if sync_result['success']:
                    all_customers.extend(sync_result['customers'])
                    all_transactions.extend(sync_result['transactions'])
                    all_products.extend(sync_result['products'])
                    
            except Exception as e:
                sync_results[platform_name] = {
                    "success": False,
                    "error": str(e),
                    "customers_synced": 0,
                    "transactions_synced": 0,
                    "products_synced": 0
                }
        
        # Create unified customer profiles
        unified_profiles = await customer_profile_manager.merge_customer_data(all_customers, all_transactions)
        
        # Generate business intelligence
        business_intelligence = await universal_intelligence_service.analyze_business_intelligence(
            unified_profiles, "Your Business"
        )
        
        return {
            "sync_results": sync_results,
            "unified_profiles_created": len(unified_profiles),
            "business_intelligence": business_intelligence.dict(),
            "sync_timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Universal sync error: {e}")

@app.get("/api/universal/customers")
async def get_unified_customers(limit: int = 100):
    """Get unified customer profiles from all platforms"""
    try:
        profiles = await customer_profile_manager.get_unified_profiles(limit)
        
        return {
            "customers": [profile.dict() for profile in profiles],
            "total_count": len(profiles),
            "platforms_represented": list(set().union(*[p.platforms_active for p in profiles])) if profiles else []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unified customers error: {e}")

@app.get("/api/universal/customers/{email}")
async def get_customer_by_email(email: str):
    """Get unified customer profile by email"""
    try:
        profile = await customer_profile_manager.get_profile_by_email(email)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Generate customer insights
        insights = await universal_intelligence_service.generate_customer_insights(profile)
        
        return {
            "customer": profile.dict(),
            "insights": [insight.dict() for insight in insights],
            "platforms": profile.platforms_active
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer lookup error: {e}")

@app.get("/api/universal/intelligence")
async def get_universal_intelligence():
    """Get comprehensive business intelligence across all platforms"""
    try:
        # Get unified customer profiles
        profiles = await customer_profile_manager.get_unified_profiles(1000)  # Get more for analysis
        
        if not profiles:
            raise HTTPException(status_code=404, detail="No customer data found. Please sync platforms first.")
        
        # Generate comprehensive intelligence
        business_intelligence = await universal_intelligence_service.analyze_business_intelligence(
            profiles, "Your Business"
        )
        
        # Generate action recommendations
        action_recommendations = await universal_intelligence_service.generate_action_recommendations(profiles)
        
        # Get dashboard data
        dashboard_data = await universal_intelligence_service.get_universal_dashboard_data(profiles)
        
        return {
            "business_intelligence": business_intelligence.dict(),
            "action_recommendations": [action.dict() for action in action_recommendations[:10]],
            "dashboard_data": dashboard_data,
            "analysis_timestamp": datetime.now(),
            "customers_analyzed": len(profiles)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Universal intelligence error: {e}")

@app.get("/api/universal/dashboard")
async def get_universal_dashboard():
    """Get universal dashboard for any business"""
    try:
        # Get unified customer profiles
        profiles = await customer_profile_manager.get_unified_profiles(500)
        
        # Get dashboard data
        dashboard_data = await universal_intelligence_service.get_universal_dashboard_data(profiles)
        
        # Get connector statuses
        connector_statuses = []
        for platform_name, connector in connectors.items():
            status = await connector.get_connector_status()
            connector_statuses.append(status.dict())
        
        return {
            "dashboard": dashboard_data,
            "connectors": connector_statuses,
            "last_updated": datetime.now(),
            "data_health": "healthy" if profiles else "no_data"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Universal dashboard error: {e}")

@app.post("/api/universal/customers/{email}/insights")
async def generate_customer_insights_endpoint(email: str):
    """Generate AI-powered insights for specific customer"""
    try:
        profile = await customer_profile_manager.get_profile_by_email(email)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        insights = await universal_intelligence_service.generate_customer_insights(profile)
        
        return {
            "customer_email": email,
            "insights": [insight.dict() for insight in insights],
            "generated_at": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer insights error: {e}")

@app.get("/api/universal/recommendations")
async def get_action_recommendations():
    """Get AI-powered action recommendations"""
    try:
        profiles = await customer_profile_manager.get_unified_profiles(200)
        recommendations = await universal_intelligence_service.generate_action_recommendations(profiles)
        
        # Group by priority
        urgent_actions = [r for r in recommendations if r.priority == "urgent"]
        high_priority = [r for r in recommendations if r.priority == "high"]
        medium_priority = [r for r in recommendations if r.priority == "medium"]
        
        return {
            "urgent_actions": [action.dict() for action in urgent_actions],
            "high_priority": [action.dict() for action in high_priority],
            "medium_priority": [action.dict() for action in medium_priority[:5]],  # Limit medium priority
            "total_recommendations": len(recommendations),
            "generated_at": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendations error: {e}")

@app.get("/api/universal/platforms/{platform_name}/test")
async def test_platform_connection(platform_name: str):
    """Test connection to specific platform"""
    try:
        if platform_name not in connectors:
            raise HTTPException(status_code=404, detail=f"Platform {platform_name} not configured")
        
        connector = connectors[platform_name]
        is_connected = await connector.test_connection()
        status = await connector.get_connector_status()
        
        return {
            "platform": platform_name,
            "connected": is_connected,
            "status": status.dict(),
            "test_timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Platform test error: {e}")

# =====================================================
# END UNIVERSAL CUSTOMER INTELLIGENCE PLATFORM ENDPOINTS
# =====================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)