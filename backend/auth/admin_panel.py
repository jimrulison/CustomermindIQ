# Admin Panel Backend System
import os
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import bcrypt
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

router = APIRouter()

# Models
class BannerRequest(BaseModel):
    title: str
    message: str
    type: str = "info"  # info, warning, success, error
    is_active: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class DiscountRequest(BaseModel):
    code: str
    discount_percentage: float
    max_uses: int
    valid_until: datetime
    is_active: bool = True

# Utility Functions
async def is_admin(user_id: str) -> bool:
    """Check if user has admin privileges"""
    user = await db.users.find_one({"id": user_id})
    return user and user.get("role") in ["admin", "super_admin"]

# Banner Management
@router.post("/banners")
async def create_banner(banner: BannerRequest):
    """Create a new system banner"""
    try:
        banner_doc = {
            "id": secrets.token_urlsafe(16),
            "title": banner.title,
            "message": banner.message,
            "type": banner.type,
            "is_active": banner.is_active,
            "start_date": banner.start_date,
            "end_date": banner.end_date,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.banners.insert_one(banner_doc)
        return {"status": "success", "banner_id": banner_doc["id"]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Banner creation failed: {str(e)}")

@router.get("/banners")
async def get_banners():
    """Get all banners"""
    try:
        banners_cursor = db.banners.find({}).sort("created_at", -1)
        banners = await banners_cursor.to_list(length=100)
        return {"status": "success", "banners": banners}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch banners: {str(e)}")

@router.get("/banners/active")
async def get_active_banners():
    """Get active banners for display"""
    try:
        now = datetime.utcnow()
        query = {
            "is_active": True,
            "$or": [
                {"start_date": None, "end_date": None},
                {"start_date": {"$lte": now}, "end_date": None},
                {"start_date": None, "end_date": {"$gte": now}},
                {"start_date": {"$lte": now}, "end_date": {"$gte": now}}
            ]
        }
        
        banners_cursor = db.banners.find(query).sort("created_at", -1)
        banners = await banners_cursor.to_list(length=10)
        return {"status": "success", "banners": banners}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch active banners: {str(e)}")

# Discount Management
@router.post("/discounts")
async def create_discount(discount: DiscountRequest):
    """Create a new discount code"""
    try:
        # Check if code already exists
        existing = await db.discounts.find_one({"code": discount.code.upper()})
        if existing:
            raise HTTPException(status_code=400, detail="Discount code already exists")
        
        discount_doc = {
            "id": secrets.token_urlsafe(16),
            "code": discount.code.upper(),
            "discount_percentage": discount.discount_percentage,
            "max_uses": discount.max_uses,
            "current_uses": 0,
            "valid_until": discount.valid_until,
            "is_active": discount.is_active,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.discounts.insert_one(discount_doc)
        return {"status": "success", "discount_id": discount_doc["id"]}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discount creation failed: {str(e)}")

@router.get("/discounts")
async def get_discounts():
    """Get all discount codes"""
    try:
        discounts_cursor = db.discounts.find({}).sort("created_at", -1)
        discounts = await discounts_cursor.to_list(length=100)
        return {"status": "success", "discounts": discounts}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch discounts: {str(e)}")

# User Management
@router.get("/users")
async def get_users():
    """Get all users with basic info"""
    try:
        users_cursor = db.users.find({}, {
            "password": 0,  # Exclude password from results
            "password_hash": 0
        }).sort("created_at", -1)
        users = await users_cursor.to_list(length=1000)
        return {"status": "success", "users": users}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

@router.put("/users/{user_id}/role")
async def update_user_role(user_id: str, role_data: dict):
    """Update user role"""
    try:
        valid_roles = ["user", "admin", "super_admin"]
        new_role = role_data.get("role")
        
        if new_role not in valid_roles:
            raise HTTPException(status_code=400, detail="Invalid role")
        
        result = await db.users.update_one(
            {"id": user_id},
            {"$set": {"role": new_role, "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"status": "success", "message": "User role updated"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Role update failed: {str(e)}")

# Analytics
@router.get("/analytics/overview")
async def get_admin_analytics():
    """Get admin dashboard analytics"""
    try:
        # User statistics
        total_users = await db.users.count_documents({})
        active_users = await db.users.count_documents({
            "last_login": {"$gte": datetime.utcnow() - timedelta(days=30)}
        })
        annual_subscribers = await db.users.count_documents({
            "subscription_tier": "annual"
        })
        
        # Banner statistics
        total_banners = await db.banners.count_documents({})
        active_banners = await db.banners.count_documents({"is_active": True})
        
        # Discount statistics
        total_discounts = await db.discounts.count_documents({})
        active_discounts = await db.discounts.count_documents({
            "is_active": True,
            "valid_until": {"$gte": datetime.utcnow()}
        })
        
        return {
            "status": "success",
            "analytics": {
                "user_stats": {
                    "total_users": total_users,
                    "active_users": active_users,
                    "annual_subscribers": annual_subscribers
                },
                "banner_stats": {
                    "total_banners": total_banners,
                    "active_banners": active_banners
                },
                "discount_stats": {
                    "total_discounts": total_discounts,
                    "active_discounts": active_discounts
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics fetch failed: {str(e)}")