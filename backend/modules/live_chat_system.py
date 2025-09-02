# Live Chat System - Premium Feature (Growth, Scale, White Label, Custom plans only)
import os
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import secrets
import json
from auth.auth_system import get_current_user, UserProfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

router = APIRouter(tags=["Live Chat"])

# Models
class ChatSession(BaseModel):
    session_id: str
    user_id: str
    user_email: str
    user_name: str
    admin_id: Optional[str] = None
    admin_name: Optional[str] = None
    status: str = "waiting"  # waiting, active, closed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    user_subscription_tier: str

class ChatMessage(BaseModel):
    message_id: str
    session_id: str
    sender_type: str  # user, admin
    sender_id: str
    sender_name: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    read_by_recipient: bool = False

class AdminAvailability(BaseModel):
    admin_id: str
    admin_email: str
    admin_name: str
    is_available: bool = True
    status_message: str = "Available for chat"
    max_concurrent_chats: int = 5
    current_active_chats: int = 0
    last_activity: datetime = Field(default_factory=datetime.utcnow)

class StartChatRequest(BaseModel):
    initial_message: Optional[str] = "Hello, I need help with my account."

class SendMessageRequest(BaseModel):
    session_id: str
    message: str

class AdminStatusUpdate(BaseModel):
    is_available: bool
    status_message: str = "Available for chat"
    max_concurrent_chats: int = 5

# WebSocket Connection Manager
class ChatConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, str] = {}  # user_id -> session_id
        self.admin_connections: Dict[str, WebSocket] = {}

    async def connect_user(self, websocket: WebSocket, user_id: str, session_id: str):
        await websocket.accept()
        self.active_connections[f"user_{user_id}"] = websocket
        self.user_sessions[user_id] = session_id

    async def connect_admin(self, websocket: WebSocket, admin_id: str):
        await websocket.accept()
        self.admin_connections[admin_id] = websocket

    def disconnect_user(self, user_id: str):
        self.active_connections.pop(f"user_{user_id}", None)
        self.user_sessions.pop(user_id, None)

    def disconnect_admin(self, admin_id: str):
        self.admin_connections.pop(admin_id, None)

    async def send_to_user(self, user_id: str, message: dict):
        connection = self.active_connections.get(f"user_{user_id}")
        if connection:
            try:
                await connection.send_text(json.dumps(message))
            except:
                self.disconnect_user(user_id)

    async def send_to_admin(self, admin_id: str, message: dict):
        connection = self.admin_connections.get(admin_id)
        if connection:
            try:
                await connection.send_text(json.dumps(message))
            except:
                self.disconnect_admin(admin_id)

    async def broadcast_to_admins(self, message: dict):
        disconnected_admins = []
        for admin_id, connection in self.admin_connections.items():
            try:
                await connection.send_text(json.dumps(message))
            except:
                disconnected_admins.append(admin_id)
        
        for admin_id in disconnected_admins:
            self.disconnect_admin(admin_id)

manager = ChatConnectionManager()

# Helper Functions
def has_premium_chat_access(user: UserProfile) -> bool:
    """
    Check if user has access to live chat feature
    Available for: Growth, Scale, White Label, Custom plans only
    NOT available for: Free trial, Launch plan
    """
    premium_tiers = ["growth", "scale", "white_label", "custom"]
    
    # Check subscription tier
    if user.subscription_tier not in premium_tiers:
        return False
    
    # Additional check: must be active subscriber (not trial)
    if hasattr(user, 'subscription_type') and user.subscription_type == "trial":
        return False
        
    return True

def require_premium_chat_access(current_user: UserProfile = Depends(get_current_user)):
    """Dependency to ensure user has premium chat access"""
    if not has_premium_chat_access(current_user):
        raise HTTPException(
            status_code=403,
            detail="Live Chat is available for Growth, Scale, White Label, and Custom plan subscribers only. Upgrade your subscription to access premium support features."
        )
    return current_user

async def get_available_admin():
    """Get an available admin for chat assignment"""
    available_admin = await db.admin_availability.find_one({
        "is_available": True,
        "current_active_chats": {"$lt": "$max_concurrent_chats"}
    })
    return available_admin

# Chat API Endpoints

@router.get("/chat/access-check")
async def check_chat_access(current_user: UserProfile = Depends(get_current_user)):
    """Check if user has access to live chat feature"""
    has_access = has_premium_chat_access(current_user)
    
    return {
        "status": "success",
        "has_access": has_access,
        "subscription_tier": current_user.subscription_tier,
        "message": "Live Chat available for Growth, Scale, White Label, and Custom plan subscribers" if has_access else "Upgrade to Growth plan or higher to access Live Chat support"
    }

@router.post("/chat/start-session")
async def start_chat_session(
    chat_request: StartChatRequest,
    current_user: UserProfile = Depends(require_premium_chat_access)
):
    """Start a new chat session (Premium subscribers only)"""
    try:
        # Check if user already has an active session
        existing_session = await db.chat_sessions.find_one({
            "user_id": current_user.user_id,
            "status": {"$in": ["waiting", "active"]}
        })
        
        if existing_session:
            return {
                "status": "success",
                "message": "Resuming existing chat session",
                "session_id": existing_session["session_id"],
                "session_status": existing_session["status"]
            }
        
        # Create new chat session
        session_id = f"chat_{secrets.token_urlsafe(16)}"
        
        chat_session = {
            "session_id": session_id,
            "user_id": current_user.user_id,
            "user_email": current_user.email,
            "user_name": f"{current_user.first_name} {current_user.last_name}",
            "status": "waiting",
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "user_subscription_tier": current_user.subscription_tier
        }
        
        await db.chat_sessions.insert_one(chat_session)
        
        # Send initial message if provided
        if chat_request.initial_message:
            message_id = f"msg_{secrets.token_urlsafe(12)}"
            initial_message = {
                "message_id": message_id,
                "session_id": session_id,
                "sender_type": "user",
                "sender_id": current_user.user_id,
                "sender_name": f"{current_user.first_name} {current_user.last_name}",
                "message": chat_request.initial_message,
                "timestamp": datetime.utcnow(),
                "read_by_recipient": False
            }
            
            await db.chat_messages.insert_one(initial_message)
        
        # Notify admins of new chat session
        await manager.broadcast_to_admins({
            "type": "new_chat_session",
            "session_id": session_id,
            "user_name": f"{current_user.first_name} {current_user.last_name}",
            "user_tier": current_user.subscription_tier,
            "initial_message": chat_request.initial_message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return {
            "status": "success",
            "message": "Chat session started successfully",
            "session_id": session_id,
            "session_status": "waiting",
            "estimated_wait_time": "2-5 minutes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start chat session: {str(e)}")

@router.post("/chat/send-message")
async def send_chat_message(
    message_request: SendMessageRequest,
    current_user: UserProfile = Depends(require_premium_chat_access)
):
    """Send a message in chat session"""
    try:
        # Verify session belongs to user
        session = await db.chat_sessions.find_one({
            "session_id": message_request.session_id,
            "user_id": current_user.user_id
        })
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        if session["status"] == "closed":
            raise HTTPException(status_code=400, detail="Chat session is closed")
        
        # Create message
        message_id = f"msg_{secrets.token_urlsafe(12)}"
        message = {
            "message_id": message_id,
            "session_id": message_request.session_id,
            "sender_type": "user",
            "sender_id": current_user.user_id,
            "sender_name": f"{current_user.first_name} {current_user.last_name}",
            "message": message_request.message,
            "timestamp": datetime.utcnow(),
            "read_by_recipient": False
        }
        
        await db.chat_messages.insert_one(message)
        
        # Update session activity
        await db.chat_sessions.update_one(
            {"session_id": message_request.session_id},
            {"$set": {"last_activity": datetime.utcnow()}}
        )
        
        # Send to admin if session is active
        if session["status"] == "active" and session.get("admin_id"):
            await manager.send_to_admin(session["admin_id"], {
                "type": "new_message",
                "session_id": message_request.session_id,
                "message": message,
                "sender_type": "user"
            })
        else:
            # Notify all admins of new message in waiting session
            await manager.broadcast_to_admins({
                "type": "new_message_waiting",
                "session_id": message_request.session_id,
                "message": message,
                "user_name": f"{current_user.first_name} {current_user.last_name}"
            })
        
        return {
            "status": "success",
            "message_id": message_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@router.get("/chat/messages/{session_id}")
async def get_chat_messages(
    session_id: str,
    current_user: UserProfile = Depends(require_premium_chat_access)
):
    """Get chat messages for a session"""
    try:
        # Verify session belongs to user
        session = await db.chat_sessions.find_one({
            "session_id": session_id,
            "user_id": current_user.user_id
        })
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Get messages
        messages = await db.chat_messages.find(
            {"session_id": session_id}
        ).sort("timestamp", 1).to_list(length=1000)
        
        # Convert ObjectId to string for JSON serialization
        for message in messages:
            message["_id"] = str(message["_id"])
            message["timestamp"] = message["timestamp"].isoformat()
        
        return {
            "status": "success",
            "session": {
                "session_id": session["session_id"],
                "status": session["status"],
                "admin_name": session.get("admin_name"),
                "created_at": session["created_at"].isoformat()
            },
            "messages": messages
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")

@router.post("/chat/close-session/{session_id}")
async def close_chat_session(
    session_id: str,
    current_user: UserProfile = Depends(require_premium_chat_access)
):
    """Close a chat session"""
    try:
        # Verify session belongs to user
        session = await db.chat_sessions.find_one({
            "session_id": session_id,
            "user_id": current_user.user_id
        })
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Close session
        await db.chat_sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "status": "closed",
                    "closed_at": datetime.utcnow(),
                    "closed_by": "user"
                }
            }
        )
        
        # Notify admin if session was active
        if session["status"] == "active" and session.get("admin_id"):
            await manager.send_to_admin(session["admin_id"], {
                "type": "session_closed",
                "session_id": session_id,
                "closed_by": "user"
            })
        
        return {
            "status": "success",
            "message": "Chat session closed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to close session: {str(e)}")

# Admin Endpoints (require admin role)

@router.get("/admin/chat/sessions")
async def get_admin_chat_sessions(
    status: Optional[str] = None,
    current_user: UserProfile = Depends(get_current_user)
):
    """Get all chat sessions for admin management"""
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        # Build query filter
        query = {}
        if status:
            query["status"] = status
        
        # Get sessions
        sessions = await db.chat_sessions.find(query).sort("created_at", -1).to_list(length=100)
        
        # Convert ObjectId and datetime for JSON
        for session in sessions:
            session["_id"] = str(session["_id"])
            session["created_at"] = session["created_at"].isoformat()
            session["last_activity"] = session["last_activity"].isoformat()
        
        return {
            "status": "success",
            "sessions": sessions,
            "total_count": len(sessions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sessions: {str(e)}")

@router.post("/admin/chat/assign-session/{session_id}")
async def assign_chat_session(
    session_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Assign a waiting chat session to admin"""
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        # Get session
        session = await db.chat_sessions.find_one({"session_id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        if session["status"] != "waiting":
            raise HTTPException(status_code=400, detail="Session is not waiting for assignment")
        
        # Assign to admin
        await db.chat_sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "admin_id": current_user.user_id,
                    "admin_name": f"{current_user.first_name} {current_user.last_name}",
                    "status": "active",
                    "assigned_at": datetime.utcnow()
                }
            }
        )
        
        # Send notification to user
        await manager.send_to_user(session["user_id"], {
            "type": "admin_joined",
            "admin_name": f"{current_user.first_name} {current_user.last_name}",
            "message": "An admin has joined your chat session"
        })
        
        return {
            "status": "success",
            "message": "Chat session assigned successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assign session: {str(e)}")

@router.post("/admin/chat/availability")
async def update_admin_availability(
    availability: AdminStatusUpdate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Update admin chat availability"""
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        # Update availability
        await db.admin_availability.update_one(
            {"admin_id": current_user.user_id},
            {
                "$set": {
                    "admin_id": current_user.user_id,
                    "admin_email": current_user.email,
                    "admin_name": f"{current_user.first_name} {current_user.last_name}",
                    "is_available": availability.is_available,
                    "status_message": availability.status_message,
                    "max_concurrent_chats": availability.max_concurrent_chats,
                    "last_activity": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        return {
            "status": "success",
            "message": "Availability updated successfully",
            "is_available": availability.is_available,
            "status_message": availability.status_message
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update availability: {str(e)}")

@router.get("/admin/chat/availability")
async def get_admin_availability():
    """Get current admin availability status (public endpoint)"""
    try:
        available_admins = await db.admin_availability.find({
            "is_available": True
        }).to_list(length=10)
        
        total_available = len(available_admins)
        estimated_wait = "2-5 minutes" if total_available > 0 else "Currently unavailable"
        
        return {
            "status": "success",
            "admins_available": total_available,
            "estimated_wait_time": estimated_wait,
            "chat_available": total_available > 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get availability: {str(e)}")

# WebSocket endpoints for real-time chat
@router.websocket("/chat/ws/{session_id}/{user_type}")
async def chat_websocket(websocket: WebSocket, session_id: str, user_type: str):
    """WebSocket endpoint for real-time chat (user_type: 'user' or 'admin')"""
    try:
        # Validate session exists
        session = await db.chat_sessions.find_one({"session_id": session_id})
        if not session:
            await websocket.close(code=4004, reason="Session not found")
            return
        
        if user_type == "user":
            user_id = session["user_id"]
            await manager.connect_user(websocket, user_id, session_id)
            
            await websocket.send_text(json.dumps({
                "type": "connection_established",
                "message": "Connected to live chat",
                "session_id": session_id
            }))
            
            try:
                while True:
                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    
                    if message_data.get("type") == "ping":
                        await websocket.send_text(json.dumps({"type": "pong"}))
                    elif message_data.get("type") == "typing":
                        # Broadcast typing indicator to admin
                        if session.get("admin_id"):
                            await manager.send_to_admin(session["admin_id"], {
                                "type": "user_typing",
                                "session_id": session_id,
                                "user_name": session["user_name"]
                            })
                    elif message_data.get("type") == "message":
                        # Handle real-time message sending
                        await handle_realtime_message(session_id, message_data, "user")
                        
            except WebSocketDisconnect:
                manager.disconnect_user(user_id)
                
        elif user_type == "admin":
            # For admin connections, we need to validate admin permissions
            # In a real implementation, you'd extract and validate the JWT token here
            admin_id = "admin_temp"  # This should come from JWT validation
            await manager.connect_admin(websocket, admin_id)
            
            await websocket.send_text(json.dumps({
                "type": "admin_connected",
                "message": "Admin connected to chat system"
            }))
            
            try:
                while True:
                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    
                    if message_data.get("type") == "ping":
                        await websocket.send_text(json.dumps({"type": "pong"}))
                    elif message_data.get("type") == "typing":
                        # Broadcast typing indicator to user
                        user_id = session["user_id"]
                        await manager.send_to_user(user_id, {
                            "type": "admin_typing",
                            "session_id": session_id,
                            "admin_name": session.get("admin_name", "Admin")
                        })
                    elif message_data.get("type") == "message":
                        # Handle real-time admin message
                        await handle_realtime_message(session_id, message_data, "admin")
                        
            except WebSocketDisconnect:
                manager.disconnect_admin(admin_id)
        else:
            await websocket.close(code=4400, reason="Invalid user type")
            
    except Exception as e:
        try:
            await websocket.close(code=4000, reason="Internal error")
        except:
            pass

async def handle_realtime_message(session_id: str, message_data: dict, sender_type: str):
    """Handle real-time message sending via WebSocket"""
    try:
        session = await db.chat_sessions.find_one({"session_id": session_id})
        if not session:
            return
        
        # Create message
        message_id = f"msg_{secrets.token_urlsafe(12)}"
        message = {
            "message_id": message_id,
            "session_id": session_id,
            "sender_type": sender_type,
            "sender_id": message_data.get("sender_id", ""),
            "sender_name": message_data.get("sender_name", ""),
            "message": message_data.get("message", ""),
            "timestamp": datetime.utcnow(),
            "read_by_recipient": False
        }
        
        # Store in database
        await db.chat_messages.insert_one(message)
        
        # Update session activity
        await db.chat_sessions.update_one(
            {"session_id": session_id},
            {"$set": {"last_activity": datetime.utcnow()}}
        )
        
        # Format message for real-time delivery
        realtime_message = {
            "type": "new_message",
            "session_id": session_id,
            "message_id": message_id,
            "sender_type": sender_type,
            "sender_name": message_data.get("sender_name", ""),
            "message": message_data.get("message", ""),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Send to appropriate recipients
        if sender_type == "user":
            # Send to admin if session is active
            if session.get("admin_id"):
                await manager.send_to_admin(session["admin_id"], realtime_message)
            else:
                # Notify all admins of new message in waiting session
                await manager.broadcast_to_admins(realtime_message)
        else:
            # Send to user
            await manager.send_to_user(session["user_id"], realtime_message)
            
    except Exception as e:
        print(f"Error handling real-time message: {e}")