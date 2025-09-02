"""
CustomerMind IQ Support System with ODOO Integration
Multi-tier support with ticketing system and admin management
"""

import asyncio
import json
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from dotenv import load_dotenv

# Import auth dependencies
from auth.auth_system import get_current_user, require_role, UserRole, UserProfile, SubscriptionTier

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

router = APIRouter(prefix="/api/support", tags=["Support"])

# Enums
class SupportTier(str, Enum):
    BASIC = "basic"           # Free trial, Starter - 24hr response
    PROFESSIONAL = "professional"  # Professional - 12hr + live chat
    ENTERPRISE = "enterprise"      # Enterprise - 4hr + live chat + CSM

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress" 
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TicketCategory(str, Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    FEATURE_REQUEST = "feature_request"
    BUG_REPORT = "bug_report"
    ACCOUNT = "account"
    GENERAL = "general"

# Models
class SupportTicketCreate(BaseModel):
    subject: str = Field(..., min_length=5, max_length=200)
    message: str = Field(..., min_length=10, max_length=5000)
    category: TicketCategory
    priority: TicketPriority = TicketPriority.MEDIUM
    attachments: Optional[List[str]] = []

class SupportTicketResponse(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    is_internal_note: bool = False

class SupportTicket(BaseModel):
    ticket_id: str
    user_id: str
    user_email: str
    subject: str
    message: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    support_tier: SupportTier
    assigned_agent: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    due_date: datetime  # Based on support tier SLA
    responses: List[Dict[str, Any]] = []
    internal_notes: List[Dict[str, Any]] = []
    odoo_ticket_id: Optional[str] = None  # For ODOO integration
    satisfaction_rating: Optional[int] = None  # 1-5 rating
    resolution_time_hours: Optional[float] = None

class LiveChatSession(BaseModel):
    session_id: str
    user_id: str
    agent_id: Optional[str] = None
    status: str  # active, waiting, ended
    created_at: datetime
    ended_at: Optional[datetime] = None
    messages: List[Dict[str, Any]] = []

# Support Tier Configuration
SUPPORT_TIER_CONFIG = {
    SupportTier.BASIC: {
        "response_time_hours": 24,
        "live_chat": False,
        "phone_support": False,
        "dedicated_csm": False,
        "priority_queue": False
    },
    SupportTier.PROFESSIONAL: {
        "response_time_hours": 12,
        "live_chat": True,
        "live_chat_hours": "9am-6pm EST (Business Hours)",
        "phone_support": False,
        "dedicated_csm": False,
        "priority_queue": True
    },
    SupportTier.ENTERPRISE: {
        "response_time_hours": 4,
        "live_chat": True,
        "live_chat_hours": "9am-6pm EST (Business Hours)",
        "phone_support": True,
        "dedicated_csm": True,
        "priority_queue": True
    }
}

# Helper Functions
def get_support_tier(subscription_tier: SubscriptionTier) -> SupportTier:
    """Map subscription tier to support tier"""
    if subscription_tier == SubscriptionTier.FREE_TRIAL:
        return SupportTier.BASIC
    elif subscription_tier == SubscriptionTier.MONTHLY:
        return SupportTier.PROFESSIONAL  
    elif subscription_tier == SubscriptionTier.ANNUAL:
        return SupportTier.ENTERPRISE
    else:
        return SupportTier.BASIC

def calculate_due_date(support_tier: SupportTier, created_at: datetime) -> datetime:
    """Calculate ticket due date based on support tier SLA"""
    response_hours = SUPPORT_TIER_CONFIG[support_tier]["response_time_hours"]
    return created_at + timedelta(hours=response_hours)

async def send_support_email(to_email: str, subject: str, body: str, ticket_id: str):
    """Send support email notification"""
    try:
        # In production, integrate with ODOO email system
        # For now, we'll log the email that would be sent
        email_log = {
            "to": to_email,
            "subject": subject,
            "body": body,
            "ticket_id": ticket_id,
            "sent_at": datetime.utcnow(),
            "type": "support_notification"
        }
        await db.email_logs.insert_one(email_log)
        print(f"Support email logged for ticket {ticket_id}: {subject}")
    except Exception as e:
        print(f"Email sending failed: {e}")

async def create_odoo_ticket(ticket_data: Dict[str, Any]) -> Optional[str]:
    """Create ticket in ODOO system (placeholder for integration)"""
    try:
        # TODO: Integrate with ODOO API
        # This would make actual API call to ODOO helpdesk module
        
        # For now, simulate ODOO integration
        odoo_ticket = {
            "odoo_ticket_id": f"ODOO-{ticket_data['ticket_id'][-8:]}",
            "subject": ticket_data["subject"],
            "description": ticket_data["message"],
            "customer_email": ticket_data["user_email"],
            "priority": ticket_data["priority"],
            "created_at": datetime.utcnow(),
            "status": "new"
        }
        
        await db.odoo_tickets.insert_one(odoo_ticket)
        return odoo_ticket["odoo_ticket_id"]
        
    except Exception as e:
        print(f"ODOO integration failed: {e}")
        return None