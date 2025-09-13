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
# Email imports removed - using logging instead of actual email sending
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

router = APIRouter(tags=["Support"])

# Enums
class SupportTier(str, Enum):
    BASIC = "basic"           # Free trial, Launch - 24hr response
    GROWTH = "growth"         # Growth - 12hr + live chat
    SCALE = "scale"           # Scale - 4hr + live chat + CSM

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
    SupportTier.GROWTH: {
        "response_time_hours": 12,
        "live_chat": True,
        "live_chat_hours": "9am-6pm EST (Business Hours)",
        "phone_support": False,
        "dedicated_csm": False,
        "priority_queue": True
    },
    SupportTier.SCALE: {
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
    if subscription_tier == SubscriptionTier.FREE:
        return SupportTier.BASIC
    elif subscription_tier in [SubscriptionTier.LAUNCH, "launch"]:
        return SupportTier.BASIC
    elif subscription_tier in [SubscriptionTier.GROWTH, "growth"]:
        return SupportTier.GROWTH  
    elif subscription_tier in [SubscriptionTier.SCALE, "scale"]:
        return SupportTier.SCALE
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

# Support Ticket Endpoints
@router.post("/tickets/create")
async def create_support_ticket(
    ticket_data: SupportTicketCreate,
    background_tasks: BackgroundTasks,
    current_user: UserProfile = Depends(get_current_user)
):
    """Create a new support ticket"""
    
    ticket_id = str(uuid.uuid4())
    support_tier = get_support_tier(current_user.subscription_tier)
    created_at = datetime.utcnow()
    due_date = calculate_due_date(support_tier, created_at)
    
    ticket = {
        "ticket_id": ticket_id,
        "user_id": current_user.user_id,
        "user_email": current_user.email,
        "subject": ticket_data.subject,
        "message": ticket_data.message,
        "category": ticket_data.category,
        "priority": ticket_data.priority,
        "status": TicketStatus.OPEN,
        "support_tier": support_tier,
        "assigned_agent": None,
        "created_at": created_at,
        "updated_at": created_at,
        "due_date": due_date,
        "responses": [],
        "internal_notes": [],
        "odoo_ticket_id": None,
        "satisfaction_rating": None,
        "resolution_time_hours": None,
        "attachments": ticket_data.attachments or []
    }
    
    # Insert ticket into database
    await db.support_tickets.insert_one(ticket)
    
    # Create ODOO ticket
    background_tasks.add_task(create_odoo_ticket, ticket)
    
    # Send confirmation email
    background_tasks.add_task(
        send_support_email,
        current_user.email,
        f"Support Ticket Created - #{ticket_id[-8:]}",
        f"Your support ticket has been created and will be responded to within {SUPPORT_TIER_CONFIG[support_tier]['response_time_hours']} hours.",
        ticket_id
    )
    
    # Remove ObjectId for response
    del ticket["_id"]
    
    return {
        "status": "success",
        "message": "Support ticket created successfully",
        "ticket": ticket,
        "support_tier_info": SUPPORT_TIER_CONFIG[support_tier]
    }

@router.get("/tickets/my")
async def get_user_tickets(
    status: Optional[TicketStatus] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: UserProfile = Depends(get_current_user)
):
    """Get user's support tickets"""
    
    query = {"user_id": current_user.user_id}
    if status:
        query["status"] = status
    
    tickets = await db.support_tickets.find(query).sort("created_at", -1).skip(offset).limit(limit).to_list(length=limit)
    total_count = await db.support_tickets.count_documents(query)
    
    # Remove ObjectIds
    for ticket in tickets:
        if "_id" in ticket:
            del ticket["_id"]
    
    return {
        "tickets": tickets,
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "support_tier": get_support_tier(current_user.subscription_tier),
        "support_tier_info": SUPPORT_TIER_CONFIG[get_support_tier(current_user.subscription_tier)]
    }

@router.get("/tickets/{ticket_id}")
async def get_ticket_details(
    ticket_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Get specific ticket details"""
    
    ticket = await db.support_tickets.find_one({"ticket_id": ticket_id, "user_id": current_user.user_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Remove ObjectId
    del ticket["_id"]
    
    return {
        "ticket": ticket,
        "support_tier_info": SUPPORT_TIER_CONFIG[ticket["support_tier"]]
    }

@router.post("/tickets/{ticket_id}/respond")
async def add_ticket_response(
    ticket_id: str,
    response_data: SupportTicketResponse,
    background_tasks: BackgroundTasks,
    current_user: UserProfile = Depends(get_current_user)
):
    """Add response to support ticket"""
    
    ticket = await db.support_tickets.find_one({"ticket_id": ticket_id, "user_id": current_user.user_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    response = {
        "response_id": str(uuid.uuid4()),
        "message": response_data.message,
        "created_by": current_user.user_id,
        "created_by_name": current_user.email,
        "created_at": datetime.utcnow(),
        "is_internal_note": response_data.is_internal_note
    }
    
    # Update ticket
    await db.support_tickets.update_one(
        {"ticket_id": ticket_id},
        {
            "$push": {"responses": response},
            "$set": {
                "updated_at": datetime.utcnow(),
                "status": TicketStatus.WAITING_CUSTOMER if ticket["status"] == TicketStatus.IN_PROGRESS else ticket["status"]
            }
        }
    )
    
    # Notify support team
    background_tasks.add_task(
        send_support_email,
        "support@customermindiq.com",  # Support team email
        f"Customer Response - Ticket #{ticket_id[-8:]}",
        f"Customer has responded to ticket: {response_data.message}",
        ticket_id
    )
    
    return {
        "status": "success",
        "message": "Response added successfully",
        "response": response
    }

# Live Chat Endpoints
@router.post("/live-chat/start")
async def start_live_chat(
    current_user: UserProfile = Depends(get_current_user)
):
    """Start live chat session"""
    
    support_tier = get_support_tier(current_user.subscription_tier)
    
    # Check if live chat is available for user's tier
    if not SUPPORT_TIER_CONFIG[support_tier]["live_chat"]:
        raise HTTPException(
            status_code=403, 
            detail=f"Live chat not available for {support_tier} tier. Please upgrade to Professional or Enterprise."
        )
    
    # Check if it's business hours (9am-6pm EST)
    # This is a simplified check - in production, use proper timezone handling
    current_hour = datetime.utcnow().hour - 5  # EST offset (simplified)
    if not (9 <= current_hour <= 18):
        raise HTTPException(
            status_code=503,
            detail="Live chat is only available during business hours (9am-6pm EST)"
        )
    
    session_id = str(uuid.uuid4())
    
    chat_session = {
        "session_id": session_id,
        "user_id": current_user.user_id,
        "user_email": current_user.email,
        "agent_id": None,
        "status": "waiting",
        "created_at": datetime.utcnow(),
        "ended_at": None,
        "messages": [],
        "support_tier": support_tier
    }
    
    await db.live_chat_sessions.insert_one(chat_session)
    
    # Remove ObjectId
    del chat_session["_id"]
    
    return {
        "status": "success",
        "message": "Live chat session started. Please wait for an agent.",
        "session": chat_session,
        "estimated_wait_time": "2-5 minutes" if support_tier == SupportTier.ENTERPRISE else "5-10 minutes"
    }

# Admin Support Management Endpoints
@router.get("/admin/tickets")
async def get_all_support_tickets(
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    support_tier: Optional[SupportTier] = None,
    assigned_agent: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all support tickets for admin management"""
    
    query = {}
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    if support_tier:
        query["support_tier"] = support_tier
    if assigned_agent:
        query["assigned_agent"] = assigned_agent
    
    tickets = await db.support_tickets.find(query).sort("created_at", -1).skip(offset).limit(limit).to_list(length=limit)
    total_count = await db.support_tickets.count_documents(query)
    
    # Remove ObjectIds
    for ticket in tickets:
        if "_id" in ticket:
            del ticket["_id"]
    
    # Get statistics
    stats = {
        "total_tickets": await db.support_tickets.count_documents({}),
        "open_tickets": await db.support_tickets.count_documents({"status": TicketStatus.OPEN}),
        "overdue_tickets": await db.support_tickets.count_documents({
            "due_date": {"$lt": datetime.utcnow()},
            "status": {"$nin": [TicketStatus.RESOLVED, TicketStatus.CLOSED]}
        }),
        "avg_resolution_time": None  # Calculate if needed
    }
    
    return {
        "tickets": tickets,
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "statistics": stats
    }

@router.put("/admin/tickets/{ticket_id}/assign")
async def assign_ticket(
    ticket_id: str,
    agent_email: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Assign ticket to support agent"""
    
    result = await db.support_tickets.update_one(
        {"ticket_id": ticket_id},
        {
            "$set": {
                "assigned_agent": agent_email,
                "status": TicketStatus.IN_PROGRESS,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {
        "status": "success",
        "message": f"Ticket assigned to {agent_email}"
    }

@router.post("/admin/tickets/{ticket_id}/respond")
async def admin_respond_to_ticket(
    ticket_id: str,
    response_data: SupportTicketResponse,
    background_tasks: BackgroundTasks,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Admin/agent response to support ticket"""
    
    ticket = await db.support_tickets.find_one({"ticket_id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    response = {
        "response_id": str(uuid.uuid4()),
        "message": response_data.message,
        "created_by": current_user.user_id,
        "created_by_name": current_user.email,
        "created_by_role": "support_agent",
        "created_at": datetime.utcnow(),
        "is_internal_note": response_data.is_internal_note
    }
    
    # Update ticket status
    new_status = TicketStatus.WAITING_CUSTOMER if not response_data.is_internal_note else ticket["status"]
    
    await db.support_tickets.update_one(
        {"ticket_id": ticket_id},
        {
            "$push": {"responses" if not response_data.is_internal_note else "internal_notes": response},
            "$set": {
                "updated_at": datetime.utcnow(),
                "status": new_status
            }
        }
    )
    
    # Send email to customer if not internal note
    if not response_data.is_internal_note:
        background_tasks.add_task(
            send_support_email,
            ticket["user_email"],
            f"Support Response - Ticket #{ticket_id[-8:]}",
            f"We have responded to your support ticket:\n\n{response_data.message}",
            ticket_id
        )
    
    return {
        "status": "success",
        "message": "Response added successfully",
        "response": response
    }

# Support Tier Information Endpoint
@router.get("/tier-info")
async def get_support_tier_info(
    current_user: UserProfile = Depends(get_current_user)
):
    """Get support tier information for current user"""
    
    support_tier = get_support_tier(current_user.subscription_tier)
    
    return {
        "support_tier": support_tier,
        "subscription_tier": current_user.subscription_tier,
        "tier_info": SUPPORT_TIER_CONFIG[support_tier],
        "upgrade_benefits": {
            "professional": SUPPORT_TIER_CONFIG[SupportTier.PROFESSIONAL] if support_tier == SupportTier.BASIC else None,
            "enterprise": SUPPORT_TIER_CONFIG[SupportTier.ENTERPRISE] if support_tier != SupportTier.ENTERPRISE else None
        }
    }