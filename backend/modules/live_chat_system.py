# Live Chat System - Premium Feature (Growth, Scale, White Label, Custom plans only)
import os
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import secrets
import json
import aiofiles
import mimetypes
from pathlib import Path
from auth.auth_system import get_current_user, UserProfile, require_role, UserRole
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

router = APIRouter(tags=["Live Chat"])

# File Upload Directory
UPLOAD_DIR = Path("/app/uploads/chat_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file types and max file size
ALLOWED_FILE_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf', 'text/plain', 'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

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
    message_type: str = "text"  # text, file, image
    file_info: Optional[Dict[str, Any]] = None  # For file messages

class FileUploadRequest(BaseModel):
    session_id: str
    file_name: str
    file_type: str
    description: Optional[str] = None

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
    Available for: Growth, Scale plans only
    NOT available for: Free trial, Launch plan
    """
    premium_tiers = ["growth", "scale"]
    
    # Check subscription tier (case-insensitive)
    user_tier = user.subscription_tier.lower() if user.subscription_tier else ""
    if user_tier not in premium_tiers:
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
            detail="Live Chat is available for Growth and Scale plan subscribers only. Upgrade your subscription to access premium support features."
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

@router.get("/chat/sessions")
async def get_user_chat_sessions(
    current_user: UserProfile = Depends(require_premium_chat_access)
):
    """Get chat sessions for the current user"""
    try:
        sessions = await db.chat_sessions.find({
            "user_id": current_user.user_id
        }).sort("created_at", -1).to_list(length=50)
        
        # Remove ObjectIds and format sessions
        for session in sessions:
            if "_id" in session:
                del session["_id"]
            
            # Get latest message preview
            latest_message = await db.chat_messages.find_one(
                {"session_id": session["session_id"]},
                sort=[("timestamp", -1)]
            )
            
            if latest_message:
                if "_id" in latest_message:
                    del latest_message["_id"]
                session["latest_message"] = latest_message
            else:
                session["latest_message"] = None
        
        return {
            "status": "success",
            "sessions": sessions,
            "total": len(sessions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get chat sessions: {str(e)}")

@router.get("/admin/chat/sessions")
async def get_admin_chat_sessions(
    status: str = None,
    limit: int = 50,
    offset: int = 0,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get chat sessions for admin management"""
    try:
        query = {}
        if status:
            query["status"] = status
            
        sessions = await db.chat_sessions.find(query).sort("created_at", -1).skip(offset).limit(limit).to_list(length=limit)
        total = await db.chat_sessions.count_documents(query)
        
        # Remove ObjectIds and enrich sessions
        for session in sessions:
            if "_id" in session:
                del session["_id"]
            
            # Get user info
            user = await db.users.find_one({"user_id": session["user_id"]})
            if user:
                session["user_info"] = {
                    "name": f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
                    "email": user.get("email"),
                    "subscription_tier": user.get("subscription_tier")
                }
            
            # Get message count
            message_count = await db.chat_messages.count_documents({"session_id": session["session_id"]})
            session["message_count"] = message_count
            
            # Get latest message
            latest_message = await db.chat_messages.find_one(
                {"session_id": session["session_id"]},
                sort=[("timestamp", -1)]
            )
            if latest_message:
                if "_id" in latest_message:
                    del latest_message["_id"]
                session["latest_message"] = latest_message
        
        return {
            "status": "success",
            "sessions": sessions,
            "total": total,
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get admin chat sessions: {str(e)}")

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

# File Sharing Endpoints

@router.post("/chat/upload-file/{session_id}")
async def upload_chat_file(
    session_id: str,
    file: UploadFile = File(...),
    current_user: UserProfile = Depends(require_premium_chat_access)
):
    """Upload a file to chat session"""
    try:
        # Verify session belongs to user
        session = await db.chat_sessions.find_one({
            "session_id": session_id,
            "user_id": current_user.user_id
        })
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        if session["status"] == "closed":
            raise HTTPException(status_code=400, detail="Cannot upload to closed session")
        
        # Validate file type
        content_type = file.content_type
        if content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"File type not allowed. Supported types: {', '.join(ALLOWED_FILE_TYPES)}"
            )
        
        # Check file size
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{secrets.token_urlsafe(16)}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Create file message
        message_id = f"msg_{secrets.token_urlsafe(12)}"
        file_info = {
            "original_name": file.filename,
            "stored_name": unique_filename,
            "content_type": content_type,
            "size": len(file_content),
            "download_url": f"/api/chat/download-file/{unique_filename}"
        }
        
        file_message = {
            "message_id": message_id,
            "session_id": session_id,
            "sender_type": "user",
            "sender_id": current_user.user_id,
            "sender_name": f"{current_user.first_name} {current_user.last_name}",
            "message": f"Shared file: {file.filename}",
            "message_type": "file",
            "file_info": file_info,
            "timestamp": datetime.utcnow(),
            "read_by_recipient": False
        }
        
        await db.chat_messages.insert_one(file_message)
        
        # Update session activity
        await db.chat_sessions.update_one(
            {"session_id": session_id},
            {"$set": {"last_activity": datetime.utcnow()}}
        )
        
        # Notify admin via WebSocket if session is active
        if session["status"] == "active" and session.get("admin_id"):
            await manager.send_to_admin(session["admin_id"], {
                "type": "file_uploaded",
                "session_id": session_id,
                "message": file_message,
                "sender_type": "user"
            })
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "message_id": message_id,
            "file_info": file_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

@router.get("/chat/download-file/{filename}")
async def download_chat_file(
    filename: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Download a chat file (requires authentication)"""
    try:
        file_path = UPLOAD_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Verify user has access to this file by checking if they're part of the session
        # In a more secure implementation, you'd store file-session mapping
        file_message = await db.chat_messages.find_one({
            "file_info.stored_name": filename
        })
        
        if not file_message:
            raise HTTPException(status_code=404, detail="File record not found")
        
        # Check if user is part of the session
        session = await db.chat_sessions.find_one({
            "session_id": file_message["session_id"]
        })
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Allow access if user is the session owner or an admin
        user_has_access = (
            session["user_id"] == current_user.user_id or 
            current_user.role in ["admin", "super_admin"]
        )
        
        if not user_has_access:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Determine content type
        content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        
        # Read and return file
        async with aiofiles.open(file_path, 'rb') as f:
            file_content = await f.read()
        
        from fastapi.responses import Response
        return Response(
            content=file_content,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={file_message['file_info']['original_name']}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")

@router.post("/admin/chat/upload-file/{session_id}")
async def admin_upload_chat_file(
    session_id: str,
    file: UploadFile = File(...),
    current_user: UserProfile = Depends(get_current_user)
):
    """Admin file upload to chat session"""
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        # Verify session exists
        session = await db.chat_sessions.find_one({"session_id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Validate file type
        content_type = file.content_type
        if content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"File type not allowed. Supported types: {', '.join(ALLOWED_FILE_TYPES)}"
            )
        
        # Check file size
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{secrets.token_urlsafe(16)}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Create file message
        message_id = f"msg_{secrets.token_urlsafe(12)}"
        file_info = {
            "original_name": file.filename,
            "stored_name": unique_filename,
            "content_type": content_type,
            "size": len(file_content),
            "download_url": f"/api/chat/download-file/{unique_filename}"
        }
        
        file_message = {
            "message_id": message_id,
            "session_id": session_id,
            "sender_type": "admin",
            "sender_id": current_user.user_id,
            "sender_name": f"{current_user.first_name} {current_user.last_name}",
            "message": f"Shared file: {file.filename}",
            "message_type": "file",
            "file_info": file_info,
            "timestamp": datetime.utcnow(),
            "read_by_recipient": False
        }
        
        await db.chat_messages.insert_one(file_message)
        
        # Update session activity
        await db.chat_sessions.update_one(
            {"session_id": session_id},
            {"$set": {"last_activity": datetime.utcnow()}}
        )
        
        # Notify user via WebSocket
        await manager.send_to_user(session["user_id"], {
            "type": "file_uploaded",
            "session_id": session_id,
            "message": file_message,
            "sender_type": "admin"
        })
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "message_id": message_id,
            "file_info": file_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

@router.get("/admin/chat/messages/{session_id}")
async def get_admin_chat_messages(
    session_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Get chat messages for admin (admin endpoint)"""
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        # Verify session exists
        session = await db.chat_sessions.find_one({"session_id": session_id})
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
                "user_name": session["user_name"],
                "admin_name": session.get("admin_name"),
                "created_at": session["created_at"].isoformat()
            },
            "messages": messages
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")

@router.post("/admin/chat/send-message")
async def admin_send_message(
    message_request: SendMessageRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """Send message as admin"""
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        # Verify session exists
        session = await db.chat_sessions.find_one({"session_id": message_request.session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        if session["status"] == "closed":
            raise HTTPException(status_code=400, detail="Chat session is closed")
        
        # Create message
        message_id = f"msg_{secrets.token_urlsafe(12)}"
        message = {
            "message_id": message_id,
            "session_id": message_request.session_id,
            "sender_type": "admin",
            "sender_id": current_user.user_id,
            "sender_name": f"{current_user.first_name} {current_user.last_name}",
            "message": message_request.message,
            "timestamp": datetime.utcnow(),
            "read_by_recipient": False
        }
        
        await db.chat_messages.insert_one(message)
        
        # Update session activity and assign admin if not already assigned
        update_data = {"last_activity": datetime.utcnow()}
        if not session.get("admin_id"):
            update_data.update({
                "admin_id": current_user.user_id,
                "admin_name": f"{current_user.first_name} {current_user.last_name}",
                "status": "active",
                "assigned_at": datetime.utcnow()
            })
        
        await db.chat_sessions.update_one(
            {"session_id": message_request.session_id},
            {"$set": update_data}
        )
        
        # Send to user via WebSocket
        await manager.send_to_user(session["user_id"], {
            "type": "new_message",
            "session_id": message_request.session_id,
            "message": message,
            "sender_type": "admin"
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