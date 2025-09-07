# Affiliate Chat System
import os
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from enum import Enum
import json

# Import authentication
from auth.auth_system import get_current_user, UserProfile, require_role, UserRole

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

router = APIRouter(prefix="/api/affiliate-chat", tags=["Affiliate Chat"])

# ========== MODELS ==========

class ChatMessageType(str, Enum):
    TEXT = "text"
    FILE = "file"
    IMAGE = "image"
    SYSTEM = "system"

class ChatSessionStatus(str, Enum):
    ACTIVE = "active"
    WAITING = "waiting"
    RESOLVED = "resolved"
    CLOSED = "closed"

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    sender_type: str  # "affiliate" or "admin"
    sender_id: str
    sender_name: str
    message_type: ChatMessageType = ChatMessageType.TEXT
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    read_by_admin: bool = False
    read_by_affiliate: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ChatSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    affiliate_id: str
    affiliate_name: str
    affiliate_email: str
    subject: str
    status: ChatSessionStatus = ChatSessionStatus.WAITING
    priority: str = "normal"  # "low", "normal", "high", "urgent"
    assigned_admin: Optional[str] = None
    assigned_admin_name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = None
    first_response_at: Optional[datetime] = None
    last_message_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    unread_count_admin: int = 0
    unread_count_affiliate: int = 0
    tags: List[str] = Field(default_factory=list)
    satisfaction_rating: Optional[int] = None
    feedback: Optional[str] = None

# Request/Response Models
class StartChatRequest(BaseModel):
    affiliate_id: str
    affiliate_name: str
    affiliate_email: str
    subject: str
    initial_message: str
    priority: str = "normal"

class SendMessageRequest(BaseModel):
    session_id: str
    content: str
    message_type: ChatMessageType = ChatMessageType.TEXT
    metadata: Dict[str, Any] = Field(default_factory=dict)

class UpdateSessionRequest(BaseModel):
    status: Optional[ChatSessionStatus] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    assigned_admin: Optional[str] = None

class FeedbackRequest(BaseModel):
    session_id: str
    satisfaction_rating: int = Field(ge=1, le=5)
    feedback: Optional[str] = None

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.admin_connections: Dict[str, WebSocket] = {}

    async def connect_affiliate(self, websocket: WebSocket, affiliate_id: str):
        await websocket.accept()
        self.active_connections[affiliate_id] = websocket

    async def connect_admin(self, websocket: WebSocket, admin_id: str):
        await websocket.accept()
        self.admin_connections[admin_id] = websocket

    def disconnect_affiliate(self, affiliate_id: str):
        if affiliate_id in self.active_connections:
            del self.active_connections[affiliate_id]

    def disconnect_admin(self, admin_id: str):
        if admin_id in self.admin_connections:
            del self.admin_connections[admin_id]

    async def send_message_to_affiliate(self, affiliate_id: str, message: dict):
        if affiliate_id in self.active_connections:
            try:
                await self.active_connections[affiliate_id].send_text(json.dumps(message))
            except:
                self.disconnect_affiliate(affiliate_id)

    async def send_message_to_admins(self, message: dict):
        disconnected_admins = []
        for admin_id, connection in self.admin_connections.items():
            try:
                await connection.send_text(json.dumps(message))
            except:
                disconnected_admins.append(admin_id)
        
        # Clean up disconnected connections
        for admin_id in disconnected_admins:
            self.disconnect_admin(admin_id)

manager = ConnectionManager()

# ========== CHAT ENDPOINTS ==========

@router.post("/sessions")
async def start_chat_session(request: StartChatRequest):
    """Start a new chat session"""
    try:
        # Create new chat session
        session = ChatSession(
            affiliate_id=request.affiliate_id,
            affiliate_name=request.affiliate_name,
            affiliate_email=request.affiliate_email,
            subject=request.subject,
            priority=request.priority,
            unread_count_admin=1  # Initial message is unread
        )
        
        # Save session to database
        session_data = session.dict()
        session_data["created_at"] = session_data["created_at"]
        session_data["updated_at"] = session_data["updated_at"]
        session_data["last_message_at"] = session_data["last_message_at"]
        
        await db.affiliate_chat_sessions.insert_one(session_data)
        
        # Create initial message
        initial_message = ChatMessage(
            session_id=session.id,
            sender_type="affiliate",
            sender_id=request.affiliate_id,
            sender_name=request.affiliate_name,
            content=request.initial_message,
            read_by_affiliate=True
        )
        
        message_data = initial_message.dict()
        message_data["timestamp"] = message_data["timestamp"]
        
        await db.affiliate_chat_messages.insert_one(message_data)
        
        # Notify all admins about new chat session
        await manager.send_message_to_admins({
            "type": "new_session",
            "session": session_data,
            "initial_message": message_data
        })
        
        return {
            "success": True,
            "session_id": session.id,
            "message": "Chat session started successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start chat session: {str(e)}")

@router.post("/messages")
async def send_message(request: SendMessageRequest, current_user: UserProfile = Depends(get_current_user)):
    """Send a message in a chat session"""
    try:
        # Get session
        session = await db.affiliate_chat_sessions.find_one({"id": request.session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Determine sender type and info
        if current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
            sender_type = "admin"
            sender_id = current_user.email
            sender_name = current_user.name or "Admin"
            read_by_admin = True
            read_by_affiliate = False
            
            # Update session - admin responded
            update_data = {
                "status": ChatSessionStatus.ACTIVE.value,
                "updated_at": datetime.now(timezone.utc),
                "last_message_at": datetime.now(timezone.utc),
                "unread_count_affiliate": session.get("unread_count_affiliate", 0) + 1
            }
            
            # Set first response time if this is the first admin response
            if not session.get("first_response_at"):
                update_data["first_response_at"] = datetime.now(timezone.utc)
                update_data["assigned_admin"] = sender_id
                update_data["assigned_admin_name"] = sender_name
            
        else:
            # Assume affiliate (in real app, you'd validate affiliate_id)
            sender_type = "affiliate"
            sender_id = session["affiliate_id"]
            sender_name = session["affiliate_name"]
            read_by_admin = False
            read_by_affiliate = True
            
            # Update session
            update_data = {
                "updated_at": datetime.now(timezone.utc),
                "last_message_at": datetime.now(timezone.utc),
                "unread_count_admin": session.get("unread_count_admin", 0) + 1
            }
        
        # Create message
        message = ChatMessage(
            session_id=request.session_id,
            sender_type=sender_type,
            sender_id=sender_id,
            sender_name=sender_name,
            message_type=request.message_type,
            content=request.content,
            read_by_admin=read_by_admin,
            read_by_affiliate=read_by_affiliate,
            metadata=request.metadata
        )
        
        # Save message
        message_data = message.dict()
        message_data["timestamp"] = message_data["timestamp"]
        await db.affiliate_chat_messages.insert_one(message_data)
        
        # Update session
        await db.affiliate_chat_sessions.update_one(
            {"id": request.session_id},
            {"$set": update_data}
        )
        
        # Send real-time updates
        if sender_type == "admin":
            # Notify affiliate
            await manager.send_message_to_affiliate(session["affiliate_id"], {
                "type": "new_message",
                "message": message_data
            })
        else:
            # Notify admins
            await manager.send_message_to_admins({
                "type": "new_message",
                "message": message_data,
                "session_id": request.session_id
            })
        
        return {
            "success": True,
            "message_id": message.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str, current_user: UserProfile = Depends(get_current_user)):
    """Get all messages for a chat session"""
    try:
        # Get session to verify access
        session = await db.affiliate_chat_sessions.find_one({"id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Get messages
        messages = await db.affiliate_chat_messages.find(
            {"session_id": session_id}
        ).sort("timestamp", 1).to_list(length=1000)
        
        # Mark messages as read based on user type
        if current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
            # Mark as read by admin
            await db.affiliate_chat_messages.update_many(
                {"session_id": session_id, "read_by_admin": False},
                {"$set": {"read_by_admin": True}}
            )
            # Reset admin unread count
            await db.affiliate_chat_sessions.update_one(
                {"id": session_id},
                {"$set": {"unread_count_admin": 0}}
            )
        
        return {
            "success": True,
            "session": session,
            "messages": messages
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")

@router.get("/sessions")
async def get_chat_sessions(
    current_user: UserProfile = Depends(get_current_user),
    status: Optional[str] = None,
    limit: int = 50
):
    """Get chat sessions (admin only)"""
    try:
        if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
            raise HTTPException(status_code=403, detail="Admin access required")
        
        query = {}
        if status:
            query["status"] = status
        
        sessions = await db.affiliate_chat_sessions.find(query).sort("updated_at", -1).limit(limit).to_list(length=limit)
        
        return {
            "success": True,
            "sessions": sessions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sessions: {str(e)}")

@router.patch("/sessions/{session_id}")
async def update_chat_session(
    session_id: str,
    request: UpdateSessionRequest,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Update chat session (admin only)"""
    try:
        update_data = {"updated_at": datetime.now(timezone.utc)}
        
        if request.status:
            update_data["status"] = request.status.value
            if request.status == ChatSessionStatus.CLOSED:
                update_data["closed_at"] = datetime.now(timezone.utc)
        
        if request.priority:
            update_data["priority"] = request.priority
        
        if request.tags is not None:
            update_data["tags"] = request.tags
        
        if request.assigned_admin:
            update_data["assigned_admin"] = request.assigned_admin
            # Get admin name (you might want to look this up from user database)
            update_data["assigned_admin_name"] = request.assigned_admin
        
        result = await db.affiliate_chat_sessions.update_one(
            {"id": session_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        return {
            "success": True,
            "message": "Session updated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update session: {str(e)}")

@router.post("/sessions/{session_id}/feedback")
async def submit_feedback(session_id: str, request: FeedbackRequest):
    """Submit feedback for a chat session"""
    try:
        update_data = {
            "satisfaction_rating": request.satisfaction_rating,
            "feedback": request.feedback,
            "updated_at": datetime.now(timezone.utc)
        }
        
        result = await db.affiliate_chat_sessions.update_one(
            {"id": session_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        return {
            "success": True,
            "message": "Feedback submitted successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")

# ========== WEBSOCKET ENDPOINTS ==========

@router.websocket("/ws/affiliate/{affiliate_id}")
async def websocket_affiliate_endpoint(websocket: WebSocket, affiliate_id: str):
    """WebSocket endpoint for affiliates"""
    await manager.connect_affiliate(websocket, affiliate_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
            message_data = json.loads(data)
            
            if message_data.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            
    except WebSocketDisconnect:
        manager.disconnect_affiliate(affiliate_id)

@router.websocket("/ws/admin/{admin_id}")
async def websocket_admin_endpoint(websocket: WebSocket, admin_id: str):
    """WebSocket endpoint for admins"""
    await manager.connect_admin(websocket, admin_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
            message_data = json.loads(data)
            
            if message_data.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            
    except WebSocketDisconnect:
        manager.disconnect_admin(admin_id)

# ========== ADMIN STATISTICS ==========

@router.get("/admin/stats")
async def get_chat_statistics(current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))):
    """Get chat statistics for admin dashboard"""
    try:
        # Get basic counts
        total_sessions = await db.affiliate_chat_sessions.count_documents({})
        waiting_sessions = await db.affiliate_chat_sessions.count_documents({"status": "waiting"})
        active_sessions = await db.affiliate_chat_sessions.count_documents({"status": "active"})
        resolved_sessions = await db.affiliate_chat_sessions.count_documents({"status": "resolved"})
        
        # Get today's sessions
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today_sessions = await db.affiliate_chat_sessions.count_documents({
            "created_at": {"$gte": today_start}
        })
        
        # Get average response time (for sessions with first_response_at)
        pipeline = [
            {"$match": {"first_response_at": {"$exists": True}}},
            {"$project": {
                "response_time": {
                    "$subtract": ["$first_response_at", "$created_at"]
                }
            }},
            {"$group": {
                "_id": None,
                "avg_response_time": {"$avg": "$response_time"}
            }}
        ]
        
        avg_response_result = await db.affiliate_chat_sessions.aggregate(pipeline).to_list(length=1)
        avg_response_time_ms = avg_response_result[0]["avg_response_time"] if avg_response_result else 0
        avg_response_time_minutes = int(avg_response_time_ms / (1000 * 60)) if avg_response_time_ms else 0
        
        # Get satisfaction ratings
        satisfaction_pipeline = [
            {"$match": {"satisfaction_rating": {"$exists": True}}},
            {"$group": {
                "_id": None,
                "avg_rating": {"$avg": "$satisfaction_rating"},
                "total_ratings": {"$sum": 1}
            }}
        ]
        
        satisfaction_result = await db.affiliate_chat_sessions.aggregate(satisfaction_pipeline).to_list(length=1)
        avg_satisfaction = satisfaction_result[0]["avg_rating"] if satisfaction_result else 0
        total_ratings = satisfaction_result[0]["total_ratings"] if satisfaction_result else 0
        
        return {
            "success": True,
            "stats": {
                "total_sessions": total_sessions,
                "waiting_sessions": waiting_sessions,
                "active_sessions": active_sessions,
                "resolved_sessions": resolved_sessions,
                "today_sessions": today_sessions,
                "avg_response_time_minutes": avg_response_time_minutes,
                "avg_satisfaction_rating": round(avg_satisfaction, 1) if avg_satisfaction else 0,
                "total_satisfaction_ratings": total_ratings
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

# ========== HELPER FUNCTIONS ==========

async def notify_admins_new_message(session_id: str, message: dict):
    """Notify all connected admins about a new message"""
    await manager.send_message_to_admins({
        "type": "new_message",
        "session_id": session_id,
        "message": message
    })

async def notify_affiliate_new_message(affiliate_id: str, message: dict):
    """Notify affiliate about a new message"""
    await manager.send_message_to_affiliate(affiliate_id, {
        "type": "new_message",
        "message": message
    })