import os
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pymongo import MongoClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json
import uuid
import logging
from enum import Enum
import smtplib
try:
    from email.mime.text import MimeText
    from email.mime.multipart import MimeMultipart
except ImportError:
    # Fallback for email functionality
    MimeText = None
    MimeMultipart = None

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CustomerHealthStatus(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good" 
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

class AlertChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    WEBHOOK = "webhook"
    IN_APP = "in_app"

# Pydantic Models
class CustomerHealthScore(BaseModel):
    customer_id: str
    health_score: float = Field(..., ge=0, le=100)
    health_status: CustomerHealthStatus
    risk_factors: List[str] = []
    positive_indicators: List[str] = []
    last_updated: datetime
    trend: str = Field(..., regex="^(improving|stable|declining)$")
    confidence: float = Field(..., ge=0, le=100)

class HealthAlert(BaseModel):
    alert_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    alert_type: str
    severity: AlertSeverity
    message: str
    created_at: datetime = Field(default_factory=datetime.now)
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    assigned_to: Optional[str] = None
    escalation_level: int = 0
    channels_sent: List[AlertChannel] = []

class EscalationRule(BaseModel):
    rule_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    conditions: Dict[str, Any]
    escalation_path: List[Dict[str, str]]  # [{"role": "csm", "email": "csm@company.com"}]
    delay_minutes: int = 30
    active: bool = True

class HealthTrigger(BaseModel):
    trigger_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    conditions: Dict[str, Any]
    actions: List[Dict[str, Any]]
    active: bool = True
    customer_segments: List[str] = []

class RealTimeCustomerHealth:
    """
    Real-Time Customer Health Monitoring & Alert System
    Provides live health scoring, automatic alerts, and escalation workflows
    """
    
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
        
        # MongoDB connection
        self.mongo_client = MongoClient(os.getenv('MONGO_URL'))
        self.db = self.mongo_client[os.getenv('DB_NAME', 'customer_intelligence')]
        
        # Collections for health monitoring
        self.health_scores_collection = self.db.customer_health_scores
        self.health_alerts_collection = self.db.health_alerts
        self.escalation_rules_collection = self.db.escalation_rules
        self.health_triggers_collection = self.db.health_triggers
        self.alert_history_collection = self.db.alert_history
        
        # WebSocket connections for real-time updates
        self.active_connections: List[WebSocket] = []
        
        # AI Health Analyzer
        self.health_analyzer = None
        
        # Background task status
        self.monitoring_active = False
        
    async def initialize_health_analyzer(self):
        """Initialize AI health analysis engine"""
        self.health_analyzer = LlmChat(
            api_key=self.api_key,
            session_id="customer_health_analysis",
            system_message="""You are an expert Customer Health Analyst specializing in real-time customer health monitoring and risk assessment.

Your expertise includes:
- Real-time customer health scoring based on multiple behavioral indicators
- Risk factor identification and trend analysis
- Early warning system for customer churn and engagement decline
- Intervention recommendations based on customer health patterns
- Escalation priority assessment for customer success teams

Always provide structured JSON responses with:
- Precise health scores (0-100)
- Clear risk factor identification
- Specific intervention recommendations
- Trend analysis (improving/stable/declining)
- Confidence levels for all assessments
- Immediate action requirements for critical situations

Focus on actionable insights that enable proactive customer success management."""
        ).with_model("openai", "gpt-4o-mini")
    
    async def calculate_real_time_health_score(self, customer_data: Dict[str, Any]) -> CustomerHealthScore:
        """
        Calculate real-time customer health score using AI analysis
        """
        if not self.health_analyzer:
            await self.initialize_health_analyzer()
        
        # Prepare comprehensive health analysis prompt
        health_prompt = f"""
        Analyze this customer's real-time health indicators and provide a comprehensive health assessment:

        Customer Profile:
        - Customer ID: {customer_data.get('customer_id', 'unknown')}
        - Name: {customer_data.get('name', 'Unknown')}
        - Total Spent: ${customer_data.get('total_spent', 0)}
        - Days Since Last Purchase: {customer_data.get('days_since_last_purchase', 0)}
        - Total Purchases: {customer_data.get('total_purchases', 0)}
        - Engagement Score: {customer_data.get('engagement_score', 0)}
        - Lifecycle Stage: {customer_data.get('lifecycle_stage', 'unknown')}
        
        Recent Activity:
        - Login Frequency: {customer_data.get('login_frequency', 'unknown')}
        - Support Tickets: {customer_data.get('recent_support_tickets', 0)}
        - Email Opens: {customer_data.get('email_opens_30d', 0)}
        - Feature Usage: {customer_data.get('feature_usage_score', 0)}
        
        Purchase History Trend:
        {json.dumps(customer_data.get('purchase_trend', []), indent=2)}
        
        Communication History:
        {json.dumps(customer_data.get('communication_history', []), indent=2)}

        Provide health analysis in this exact JSON format:
        {{
            "customer_id": "{customer_data.get('customer_id', 'unknown')}",
            "health_score": 0-100,
            "health_status": "excellent|good|fair|poor|critical",
            "risk_factors": [
                "specific risk factor 1",
                "specific risk factor 2"
            ],
            "positive_indicators": [
                "positive indicator 1", 
                "positive indicator 2"
            ],
            "trend": "improving|stable|declining",
            "confidence": 0-100,
            "immediate_actions_required": [
                {{
                    "action": "specific action needed",
                    "priority": "high|medium|low",
                    "timeline": "immediate|24h|1week"
                }}
            ],
            "intervention_recommendations": [
                {{
                    "type": "email|call|meeting|offer",
                    "message": "specific recommendation",
                    "expected_impact": "description"
                }}
            ],
            "escalation_required": true/false,
            "escalation_reason": "reason if escalation needed"
        }}
        """
        
        try:
            user_message = UserMessage(text=health_prompt)
            response = await self.health_analyzer.send_message(user_message)
            
            # Parse AI response
            health_data = self._parse_json_response(response)
            
            # Create CustomerHealthScore object
            health_score = CustomerHealthScore(
                customer_id=customer_data.get('customer_id', 'unknown'),
                health_score=health_data.get('health_score', 50),
                health_status=CustomerHealthStatus(health_data.get('health_status', 'fair')),
                risk_factors=health_data.get('risk_factors', []),
                positive_indicators=health_data.get('positive_indicators', []),
                last_updated=datetime.now(),
                trend=health_data.get('trend', 'stable'),
                confidence=health_data.get('confidence', 50)
            )
            
            # Store in database
            health_record = health_score.dict()
            health_record['_id'] = f"{health_score.customer_id}_{int(datetime.now().timestamp())}"
            health_record['ai_analysis'] = health_data
            
            # Update or insert health score
            self.health_scores_collection.replace_one(
                {"customer_id": health_score.customer_id},
                health_record,
                upsert=True
            )
            
            # Check for alerts
            await self._check_health_alerts(health_score, health_data)
            
            return health_score
            
        except Exception as e:
            logger.error(f"Error calculating health score for customer {customer_data.get('customer_id')}: {str(e)}")
            # Return basic health score
            return CustomerHealthScore(
                customer_id=customer_data.get('customer_id', 'unknown'),
                health_score=50,
                health_status=CustomerHealthStatus.FAIR,
                risk_factors=["Analysis unavailable"],
                positive_indicators=[],
                last_updated=datetime.now(),
                trend="stable",
                confidence=25
            )
    
    async def _check_health_alerts(self, health_score: CustomerHealthScore, ai_analysis: Dict[str, Any]):
        """Check if health score triggers any alerts"""
        alerts_to_send = []
        
        # Critical health score alert
        if health_score.health_score < 30:
            alert = HealthAlert(
                customer_id=health_score.customer_id,
                alert_type="critical_health_decline",
                severity=AlertSeverity.CRITICAL,
                message=f"Customer health critically low: {health_score.health_score}/100. Immediate intervention required."
            )
            alerts_to_send.append(alert)
        
        # Declining trend alert
        elif health_score.trend == "declining" and health_score.health_score < 60:
            alert = HealthAlert(
                customer_id=health_score.customer_id,
                alert_type="declining_health_trend",
                severity=AlertSeverity.HIGH,
                message=f"Customer health declining: {health_score.health_score}/100. Proactive outreach recommended."
            )
            alerts_to_send.append(alert)
        
        # High risk factors alert
        elif len(health_score.risk_factors) >= 3:
            alert = HealthAlert(
                customer_id=health_score.customer_id,
                alert_type="multiple_risk_factors",
                severity=AlertSeverity.MEDIUM,
                message=f"Multiple risk factors detected: {', '.join(health_score.risk_factors[:3])}"
            )
            alerts_to_send.append(alert)
        
        # Escalation required alert
        if ai_analysis.get('escalation_required', False):
            alert = HealthAlert(
                customer_id=health_score.customer_id,
                alert_type="escalation_required",
                severity=AlertSeverity.HIGH,
                message=f"Escalation required: {ai_analysis.get('escalation_reason', 'AI recommends escalation')}"
            )
            alerts_to_send.append(alert)
        
        # Send alerts
        for alert in alerts_to_send:
            await self._send_alert(alert)
    
    async def _send_alert(self, alert: HealthAlert):
        """Send alert through configured channels"""
        try:
            # Store alert in database
            alert_record = alert.dict()
            alert_record['_id'] = alert.alert_id
            self.health_alerts_collection.insert_one(alert_record)
            
            # Send through real-time WebSocket
            await self._broadcast_alert(alert)
            
            # Send through configured channels (email, etc.)
            await self._send_alert_notifications(alert)
            
            # Check for escalation rules
            await self._check_escalation_rules(alert)
            
            logger.info(f"Alert sent for customer {alert.customer_id}: {alert.message}")
            
        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")
    
    async def _broadcast_alert(self, alert: HealthAlert):
        """Broadcast alert to all connected WebSocket clients"""
        if self.active_connections:
            alert_data = {
                "type": "health_alert",
                "data": alert.dict(),
                "timestamp": datetime.now().isoformat()
            }
            
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(alert_data))
                except:
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for conn in disconnected:
                self.active_connections.remove(conn)
    
    async def _send_alert_notifications(self, alert: HealthAlert):
        """Send alert notifications via email/SMS/Slack"""
        # This would integrate with actual notification services
        # For now, we'll log the notification
        logger.info(f"Notification sent: {alert.severity} alert for customer {alert.customer_id}")
        
        # Mark channels as sent
        alert.channels_sent.append(AlertChannel.IN_APP)
    
    async def _check_escalation_rules(self, alert: HealthAlert):
        """Check if alert matches any escalation rules"""
        rules = list(self.escalation_rules_collection.find({"active": True}))
        
        for rule_data in rules:
            rule = EscalationRule(**rule_data)
            
            # Simple rule matching (can be enhanced)
            if alert.severity.value in rule.conditions.get('severities', []):
                await self._trigger_escalation(alert, rule)
    
    async def _trigger_escalation(self, alert: HealthAlert, rule: EscalationRule):
        """Trigger escalation workflow"""
        logger.info(f"Escalation triggered for alert {alert.alert_id} using rule {rule.name}")
        
        # Update alert with escalation info
        self.health_alerts_collection.update_one(
            {"_id": alert.alert_id},
            {"$set": {"escalation_level": alert.escalation_level + 1}}
        )
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response"""
        try:
            # Clean the response
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:-3]
            elif cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:-3]
            
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return {"error": "Failed to parse AI response"}
    
    async def get_customer_health_dashboard(self, limit: int = 50) -> Dict[str, Any]:
        """Get real-time customer health dashboard data"""
        try:
            # Get recent health scores
            health_scores = list(self.health_scores_collection.find({}).sort("last_updated", -1).limit(limit))
            
            # Calculate summary statistics
            total_customers = len(health_scores)
            if total_customers == 0:
                return {
                    "summary": {"total_customers": 0, "message": "No customer health data available"},
                    "health_distribution": {},
                    "alerts": [],
                    "trends": {}
                }
            
            # Health distribution
            health_distribution = {}
            risk_customers = []
            declining_customers = []
            
            for score in health_scores:
                status = score.get('health_status', 'fair')
                health_distribution[status] = health_distribution.get(status, 0) + 1
                
                if score.get('health_score', 50) < 40:
                    risk_customers.append(score)
                
                if score.get('trend') == 'declining':
                    declining_customers.append(score)
            
            # Recent alerts
            recent_alerts = list(self.health_alerts_collection.find({
                "resolved": False
            }).sort("created_at", -1).limit(10))
            
            # Average health score
            avg_health = sum([s.get('health_score', 50) for s in health_scores]) / total_customers
            
            dashboard_data = {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_customers": total_customers,
                    "average_health_score": round(avg_health, 1),
                    "at_risk_customers": len(risk_customers),
                    "declining_trend_customers": len(declining_customers),
                    "active_alerts": len(recent_alerts)
                },
                "health_distribution": health_distribution,
                "top_risk_customers": [
                    {
                        "customer_id": c['customer_id'],
                        "health_score": c.get('health_score', 0),
                        "risk_factors": c.get('risk_factors', [])[:3]
                    }
                    for c in sorted(risk_customers, key=lambda x: x.get('health_score', 0))[:5]
                ],
                "recent_alerts": [
                    {
                        "alert_id": a['alert_id'],
                        "customer_id": a['customer_id'],
                        "severity": a['severity'],
                        "message": a['message'],
                        "created_at": a['created_at'].isoformat()
                    }
                    for a in recent_alerts
                ],
                "trends": {
                    "improving": len([s for s in health_scores if s.get('trend') == 'improving']),
                    "stable": len([s for s in health_scores if s.get('trend') == 'stable']),
                    "declining": len([s for s in health_scores if s.get('trend') == 'declining'])
                }
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error generating health dashboard: {str(e)}")
            return {"error": "Dashboard generation failed", "details": str(e)}

# Create global instance
real_time_health_monitor = RealTimeCustomerHealth()

# FastAPI Router
router = APIRouter(prefix="/api/customer-health", tags=["Real-Time Customer Health"])

@router.get("/dashboard")
async def get_health_dashboard(limit: int = 50):
    """Get real-time customer health dashboard"""
    try:
        dashboard = await real_time_health_monitor.get_customer_health_dashboard(limit)
        return dashboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {str(e)}")

@router.get("/customer/{customer_id}/health")
async def get_customer_health(customer_id: str):
    """Get specific customer's current health score"""
    try:
        health_record = real_time_health_monitor.health_scores_collection.find_one(
            {"customer_id": customer_id}
        )
        
        if not health_record:
            raise HTTPException(status_code=404, detail="Customer health data not found")
        
        return {
            "customer_id": customer_id,
            "health_score": health_record.get('health_score', 0),
            "health_status": health_record.get('health_status', 'unknown'),
            "risk_factors": health_record.get('risk_factors', []),
            "positive_indicators": health_record.get('positive_indicators', []),
            "trend": health_record.get('trend', 'stable'),
            "last_updated": health_record.get('last_updated', datetime.now()).isoformat(),
            "ai_recommendations": health_record.get('ai_analysis', {}).get('intervention_recommendations', [])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health retrieval failed: {str(e)}")

@router.post("/customer/{customer_id}/calculate-health")
async def calculate_customer_health(customer_id: str, customer_data: Dict[str, Any]):
    """Calculate real-time health score for a customer"""
    try:
        customer_data['customer_id'] = customer_id
        health_score = await real_time_health_monitor.calculate_real_time_health_score(customer_data)
        return health_score.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health calculation failed: {str(e)}")

@router.get("/alerts")
async def get_active_alerts(limit: int = 20):
    """Get active health alerts"""
    try:
        alerts = list(real_time_health_monitor.health_alerts_collection.find({
            "resolved": False
        }).sort("created_at", -1).limit(limit))
        
        return {
            "alerts": [
                {
                    "alert_id": a['alert_id'],
                    "customer_id": a['customer_id'],
                    "alert_type": a['alert_type'],
                    "severity": a['severity'],
                    "message": a['message'],
                    "created_at": a['created_at'].isoformat(),
                    "escalation_level": a.get('escalation_level', 0)
                }
                for a in alerts
            ],
            "total_active_alerts": len(alerts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alert retrieval failed: {str(e)}")

@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    """Mark an alert as resolved"""
    try:
        result = real_time_health_monitor.health_alerts_collection.update_one(
            {"alert_id": alert_id},
            {
                "$set": {
                    "resolved": True,
                    "resolved_at": datetime.now()
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {"message": "Alert resolved successfully", "alert_id": alert_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alert resolution failed: {str(e)}")

@router.websocket("/ws/health-monitoring")
async def websocket_health_monitoring(websocket: WebSocket):
    """WebSocket endpoint for real-time health monitoring"""
    await websocket.accept()
    real_time_health_monitor.active_connections.append(websocket)
    
    try:
        while True:
            # Keep connection alive and send periodic updates
            await asyncio.sleep(30)  # Send updates every 30 seconds
            
            # Send health summary
            try:
                dashboard = await real_time_health_monitor.get_customer_health_dashboard()
                await websocket.send_text(json.dumps({
                    "type": "health_update",
                    "data": dashboard,
                    "timestamp": datetime.now().isoformat()
                }))
            except:
                break
                
    except WebSocketDisconnect:
        real_time_health_monitor.active_connections.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        if websocket in real_time_health_monitor.active_connections:
            real_time_health_monitor.active_connections.remove(websocket)