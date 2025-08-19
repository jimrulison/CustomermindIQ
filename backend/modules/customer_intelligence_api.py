from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging

from .ai_customer_intelligence import ai_customer_intelligence
from .odoo_integration import odoo_integration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/customer-intelligence", tags=["Customer Intelligence"])

@router.get("/status")
async def get_system_status():
    """Get overall system status including ODOO and AI connections"""
    try:
        # Test ODOO connection
        odoo_status = odoo_integration.test_connection()
        
        # Test AI system (simple initialization check)
        try:
            await ai_customer_intelligence.initialize_ai_engines()
            ai_status = {"status": "operational", "message": "AI engines initialized successfully"}
        except Exception as e:
            ai_status = {"status": "error", "message": f"AI initialization failed: {str(e)}"}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_status": "operational" if odoo_status['connected'] and ai_status['status'] == 'operational' else "degraded",
            "odoo_integration": odoo_status,
            "ai_system": ai_status,
            "capabilities": [
                "Customer Behavior Analysis",
                "Purchase Prediction", 
                "Product Recommendations",
                "Business Rules Generation",
                "ODOO Data Integration",
                "Email Automation"
            ]
        }
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"System status check failed: {str(e)}")

@router.get("/customers")
async def get_customers(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    include_analysis: bool = Query(default=False)
):
    """Get customers from ODOO with optional AI analysis"""
    try:
        # Get customers from ODOO
        customers = odoo_integration.get_customers(limit=limit, offset=offset)
        
        if not customers:
            return {
                "customers": [],
                "total": 0,
                "message": "No customers found"
            }
        
        # Enhance with purchase history and AI analysis if requested
        enhanced_customers = []
        for customer in customers:
            # Get purchase history
            purchase_history = odoo_integration.get_customer_purchase_history(
                customer_id=int(customer['customer_id'])
            )
            customer['purchase_history'] = purchase_history
            
            # Calculate additional metrics
            if purchase_history:
                customer['total_purchases'] = len(purchase_history)
                customer['last_purchase_date'] = max([order['date'] for order in purchase_history])
                customer['average_order_value'] = sum([order['total_amount'] for order in purchase_history]) / len(purchase_history)
            else:
                customer['total_purchases'] = 0
                customer['last_purchase_date'] = None
                customer['average_order_value'] = 0
            
            # Add AI analysis if requested
            if include_analysis:
                try:
                    ai_analysis = await ai_customer_intelligence.analyze_customer_behavior(customer)
                    customer['ai_analysis'] = ai_analysis
                except Exception as e:
                    logger.warning(f"AI analysis failed for customer {customer['customer_id']}: {str(e)}")
                    customer['ai_analysis'] = {"error": "AI analysis unavailable"}
            
            enhanced_customers.append(customer)
        
        return {
            "customers": enhanced_customers,
            "total": len(enhanced_customers),
            "limit": limit,
            "offset": offset,
            "includes_ai_analysis": include_analysis
        }
        
    except Exception as e:
        logger.error(f"Error retrieving customers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve customers: {str(e)}")

@router.get("/customers/{customer_id}/analysis")
async def analyze_customer(customer_id: str):
    """Get comprehensive AI analysis for a specific customer"""
    try:
        # Get customer data from ODOO
        customers = odoo_integration.get_customers(limit=1000)  # Get all to find specific customer
        customer_data = next((c for c in customers if c['customer_id'] == customer_id), None)
        
        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Get purchase history
        purchase_history = odoo_integration.get_customer_purchase_history(
            customer_id=int(customer_id)
        )
        customer_data['purchase_history'] = purchase_history
        
        # Perform AI analysis
        analysis = await ai_customer_intelligence.analyze_customer_behavior(customer_data)
        
        return {
            "customer_id": customer_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "customer_profile": customer_data,
            "ai_analysis": analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing customer {customer_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Customer analysis failed: {str(e)}")

@router.get("/customers/{customer_id}/predictions")
async def predict_customer_behavior(customer_id: str):
    """Get AI predictions for customer's next purchase behavior"""
    try:
        # Get customer data
        customers = odoo_integration.get_customers(limit=1000)
        customer_data = next((c for c in customers if c['customer_id'] == customer_id), None)
        
        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Get purchase history and enhance data
        purchase_history = odoo_integration.get_customer_purchase_history(
            customer_id=int(customer_id)
        )
        
        # Prepare data for prediction
        customer_data['purchase_history'] = purchase_history
        if purchase_history:
            customer_data['recent_purchases'] = purchase_history[-5:]  # Last 5 purchases
            last_purchase = max(purchase_history, key=lambda x: x['date'])
            last_purchase_date = datetime.fromisoformat(last_purchase['date'].replace('Z', '+00:00'))
            customer_data['days_since_last_purchase'] = (datetime.now() - last_purchase_date.replace(tzinfo=None)).days
        else:
            customer_data['recent_purchases'] = []
            customer_data['days_since_last_purchase'] = 999
        
        # Get AI predictions
        predictions = await ai_customer_intelligence.predict_next_purchase(customer_data)
        
        return {
            "customer_id": customer_id,
            "prediction_timestamp": datetime.now().isoformat(),
            "predictions": predictions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error predicting customer behavior for {customer_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/customers/{customer_id}/recommendations")
async def get_customer_recommendations(customer_id: str):
    """Get AI-powered product recommendations for a customer"""
    try:
        # Get customer data
        customers = odoo_integration.get_customers(limit=1000)
        customer_data = next((c for c in customers if c['customer_id'] == customer_id), None)
        
        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Get purchase history
        purchase_history = odoo_integration.get_customer_purchase_history(
            customer_id=int(customer_id)
        )
        customer_data['purchase_history'] = purchase_history
        
        # Get available products
        available_products = odoo_integration.get_products(limit=100)
        
        # Generate recommendations
        recommendations = await ai_customer_intelligence.generate_product_recommendations(
            customer_data, available_products
        )
        
        return {
            "customer_id": customer_id,
            "recommendation_timestamp": datetime.now().isoformat(),
            "recommendations": recommendations,
            "available_products_count": len(available_products)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendations for {customer_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")

@router.post("/customers/batch-analysis")
async def batch_analyze_customers(
    background_tasks: BackgroundTasks,
    customer_ids: Optional[List[str]] = None,
    limit: int = Query(default=50, ge=1, le=200)
):
    """Perform batch AI analysis on multiple customers"""
    try:
        # Get customers to analyze
        if customer_ids:
            customers = odoo_integration.get_customers(limit=1000)
            target_customers = [c for c in customers if c['customer_id'] in customer_ids]
        else:
            target_customers = odoo_integration.get_customers(limit=limit)
        
        if not target_customers:
            return {
                "message": "No customers found for analysis",
                "analyzed_count": 0
            }
        
        # Perform analysis (async for better performance)
        analysis_results = []
        for customer in target_customers[:limit]:  # Respect limit
            try:
                # Get purchase history
                purchase_history = odoo_integration.get_customer_purchase_history(
                    customer_id=int(customer['customer_id'])
                )
                customer['purchase_history'] = purchase_history
                
                # Perform AI analysis
                analysis = await ai_customer_intelligence.analyze_customer_behavior(customer)
                
                analysis_results.append({
                    "customer_id": customer['customer_id'],
                    "status": "success",
                    "analysis": analysis
                })
            except Exception as e:
                logger.warning(f"Analysis failed for customer {customer['customer_id']}: {str(e)}")
                analysis_results.append({
                    "customer_id": customer['customer_id'],
                    "status": "failed",
                    "error": str(e)
                })
        
        return {
            "batch_analysis_timestamp": datetime.now().isoformat(),
            "analyzed_count": len(analysis_results),
            "success_count": len([r for r in analysis_results if r['status'] == 'success']),
            "failed_count": len([r for r in analysis_results if r['status'] == 'failed']),
            "results": analysis_results
        }
        
    except Exception as e:
        logger.error(f"Batch analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@router.get("/business-rules")
async def get_business_rules():
    """Get AI-generated business rules based on customer data patterns"""
    try:
        # Get sample of customer data for analysis
        customers = odoo_integration.get_customers(limit=100)
        
        # Calculate business context
        total_customers = len(customers)
        total_revenue = sum([float(c.get('total_spent', 0)) for c in customers])
        avg_revenue_per_customer = total_revenue / total_customers if total_customers > 0 else 0
        
        # Analyze customer patterns
        lifecycle_distribution = {}
        engagement_distribution = {}
        
        for customer in customers:
            stage = customer.get('lifecycle_stage', 'unknown')
            lifecycle_distribution[stage] = lifecycle_distribution.get(stage, 0) + 1
            
            score_range = 'high' if customer.get('engagement_score', 0) > 70 else 'medium' if customer.get('engagement_score', 0) > 40 else 'low'
            engagement_distribution[score_range] = engagement_distribution.get(score_range, 0) + 1
        
        business_context = {
            'industry': 'Software/Technology',
            'business_model': 'B2B SaaS',
            'customer_count': total_customers,
            'arpc': avg_revenue_per_customer,
            'cac': 150,  # Estimated
            'churn_rate': 5,  # Estimated
            'customer_patterns': {
                'lifecycle_distribution': lifecycle_distribution,
                'engagement_distribution': engagement_distribution,
                'average_revenue_per_customer': avg_revenue_per_customer
            }
        }
        
        # Generate AI business rules
        business_rules = await ai_customer_intelligence.generate_business_rules(business_context)
        
        return {
            "generation_timestamp": datetime.now().isoformat(),
            "business_context": business_context,
            "ai_generated_rules": business_rules
        }
        
    except Exception as e:
        logger.error(f"Error generating business rules: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Business rules generation failed: {str(e)}")

@router.get("/cohort-analysis")
async def analyze_customer_cohort(
    cohort_size: int = Query(default=50, ge=10, le=200),
    lifecycle_stage: Optional[str] = Query(default=None)
):
    """Perform AI analysis on a customer cohort"""
    try:
        # Get customer cohort
        customers = odoo_integration.get_customers(limit=cohort_size * 2)  # Get more to filter
        
        # Filter by lifecycle stage if specified
        if lifecycle_stage:
            customers = [c for c in customers if c.get('lifecycle_stage') == lifecycle_stage]
        
        # Limit to requested cohort size
        cohort = customers[:cohort_size]
        
        if not cohort:
            return {
                "message": "No customers found for cohort analysis",
                "cohort_size": 0
            }
        
        # Enhance cohort data with purchase history
        for customer in cohort:
            purchase_history = odoo_integration.get_customer_purchase_history(
                customer_id=int(customer['customer_id']),
                days_back=365
            )
            customer['purchase_history'] = purchase_history
        
        # Perform AI cohort analysis
        cohort_analysis = await ai_customer_intelligence.analyze_customer_cohort(cohort)
        
        return {
            "cohort_analysis_timestamp": datetime.now().isoformat(),
            "requested_cohort_size": cohort_size,
            "actual_cohort_size": len(cohort),
            "lifecycle_stage_filter": lifecycle_stage,
            "analysis": cohort_analysis
        }
        
    except Exception as e:
        logger.error(f"Cohort analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cohort analysis failed: {str(e)}")

@router.get("/insights/dashboard")
async def get_intelligence_dashboard():
    """Get comprehensive customer intelligence dashboard data"""
    try:
        # Get recent customers for analysis
        customers = odoo_integration.get_customers(limit=100)
        
        if not customers:
            return {
                "message": "No customer data available",
                "dashboard_data": {}
            }
        
        # Calculate key metrics
        total_customers = len(customers)
        total_revenue = sum([float(c.get('total_spent', 0)) for c in customers])
        avg_customer_value = total_revenue / total_customers if total_customers > 0 else 0
        
        # Lifecycle stage distribution
        lifecycle_distribution = {}
        engagement_distribution = {'high': 0, 'medium': 0, 'low': 0}
        churn_risk_distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for customer in customers:
            # Lifecycle stages
            stage = customer.get('lifecycle_stage', 'unknown')
            lifecycle_distribution[stage] = lifecycle_distribution.get(stage, 0) + 1
            
            # Engagement distribution
            engagement_score = customer.get('engagement_score', 0)
            if engagement_score > 70:
                engagement_distribution['high'] += 1
            elif engagement_score > 40:
                engagement_distribution['medium'] += 1
            else:
                engagement_distribution['low'] += 1
            
            # Estimated churn risk distribution (simplified)
            days_since_reg = customer.get('days_since_registration', 0)
            total_spent = float(customer.get('total_spent', 0))
            
            if total_spent == 0 and days_since_reg > 30:
                churn_risk_distribution['high'] += 1
            elif total_spent < avg_customer_value * 0.5:
                churn_risk_distribution['medium'] += 1
            else:
                churn_risk_distribution['low'] += 1
        
        # Get top customers by value
        top_customers = sorted(customers, key=lambda x: float(x.get('total_spent', 0)), reverse=True)[:10]
        
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "summary_metrics": {
                "total_customers": total_customers,
                "total_revenue": round(total_revenue, 2),
                "average_customer_value": round(avg_customer_value, 2),
                "new_customers_this_month": len([c for c in customers if c.get('lifecycle_stage') == 'new'])
            },
            "customer_segmentation": {
                "lifecycle_stages": lifecycle_distribution,
                "engagement_levels": engagement_distribution,
                "churn_risk_levels": churn_risk_distribution
            },
            "top_customers": [
                {
                    "customer_id": c['customer_id'],
                    "name": c['name'],
                    "total_spent": c['total_spent'],
                    "engagement_score": c.get('engagement_score', 0),
                    "lifecycle_stage": c.get('lifecycle_stage', 'unknown')
                }
                for c in top_customers
            ],
            "intelligence_insights": [
                f"Top 10% of customers generate ${round(sum([float(c.get('total_spent', 0)) for c in top_customers[:max(1, total_customers//10)]]), 2)} in revenue",
                f"{engagement_distribution['high']} customers show high engagement levels",
                f"{churn_risk_distribution['high']} customers are at high risk of churning",
                f"Average customer lifetime value: ${round(avg_customer_value, 2)}"
            ]
        }
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Dashboard data generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {str(e)}")

@router.post("/email/send")
async def send_intelligent_email(
    customer_id: str,
    email_type: str = Query(..., description="welcome|retention|upsell|custom"),
    custom_subject: Optional[str] = None,
    custom_content: Optional[str] = None
):
    """Send AI-generated intelligent email to customer"""
    try:
        # Get customer data
        customers = odoo_integration.get_customers(limit=1000)
        customer_data = next((c for c in customers if c['customer_id'] == customer_id), None)
        
        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        if not customer_data.get('email'):
            raise HTTPException(status_code=400, detail="Customer email not available")
        
        # Generate email content based on type
        if email_type == "custom" and custom_subject and custom_content:
            subject = custom_subject
            content = custom_content
        else:
            # For now, use simple templates (can be enhanced with AI generation later)
            email_templates = {
                "welcome": {
                    "subject": f"Welcome to Customer Mind IQ, {customer_data['name']}!",
                    "content": f"<h1>Welcome {customer_data['name']}</h1><p>Thank you for joining Customer Mind IQ. We're excited to help you optimize your customer intelligence.</p>"
                },
                "retention": {
                    "subject": f"We miss you, {customer_data['name']}",
                    "content": f"<h1>Hi {customer_data['name']}</h1><p>We've noticed you haven't been active lately. Let us help you get the most out of our platform.</p>"
                },
                "upsell": {
                    "subject": f"Unlock more value, {customer_data['name']}",
                    "content": f"<h1>Hi {customer_data['name']}</h1><p>Based on your usage patterns, you might benefit from our advanced features.</p>"
                }
            }
            
            template = email_templates.get(email_type, email_templates["welcome"])
            subject = template["subject"]
            content = template["content"]
        
        # Send email via ODOO
        success = odoo_integration.send_email(
            recipient_email=customer_data['email'],
            subject=subject,
            body=content
        )
        
        if success:
            return {
                "timestamp": datetime.now().isoformat(),
                "customer_id": customer_id,
                "email": customer_data['email'],
                "email_type": email_type,
                "status": "sent",
                "subject": subject
            }
        else:
            raise HTTPException(status_code=500, detail="Email sending failed")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")