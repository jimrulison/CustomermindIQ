"""
Support System Module
Handles FAQ, contact forms, community posts, and admin functions
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import asyncio

router = APIRouter()

# Pydantic Models
class ContactForm(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    subject: Optional[str] = None
    comments: Optional[str] = None

class CommunityPost(BaseModel):
    title: str
    content: str
    type: str = "question"  # question, suggestion, issue, announcement
    author: Optional[str] = "Anonymous"

class Announcement(BaseModel):
    message: str
    type: str = "info"  # info, warning, error, success
    active: bool = True
    dismissible: bool = True

# Mock Database
COMMUNITY_POSTS = []
ANNOUNCEMENTS = []
CONTACT_REQUESTS = []

# Initialize with demo data
def init_demo_data():
    global COMMUNITY_POSTS, ANNOUNCEMENTS
    
    COMMUNITY_POSTS = [
        {
            "id": 1,
            "title": "Feature Request: Bulk Website Import",
            "content": "It would be great to have a CSV import feature for adding multiple websites at once, especially for agencies managing many client sites.",
            "type": "suggestion",
            "author": "Sarah Chen",
            "date": "2024-12-15",
            "replies": 3,
            "likes": 8,
            "isPinned": False,
            "isVisible": True
        },
        {
            "id": 2,
            "title": "Issue: Performance scores not updating",
            "content": "I've noticed that my performance scores haven't updated in 3 days despite clicking 'Update All' several times. All other metrics are updating normally.",
            "type": "issue",
            "author": "Mike Rodriguez",
            "date": "2024-12-14",
            "replies": 1,
            "likes": 2,
            "isPinned": False,
            "isVisible": True
        },
        {
            "id": 3,
            "title": "📋 PINNED: Upcoming Training Sessions",
            "content": "Join us for upcoming training sessions:\n• Advanced SEO Strategies - Dec 20, 2PM EST\n• Multi-Website Management - Dec 22, 1PM EST\n• Performance Optimization Workshop - Dec 27, 3PM EST\n\nRegister at training@customermindiq.com",
            "type": "announcement",
            "author": "CustomerMind IQ Team",
            "date": "2024-12-13",
            "replies": 5,
            "likes": 15,
            "isPinned": True,
            "isVisible": True
        }
    ]
    
    ANNOUNCEMENTS = [
        {
            "id": 1,
            "message": "🎓 New Training Session: Advanced SEO Strategies - December 20, 2PM EST. Register now!",
            "type": "info",
            "active": True,
            "dismissible": True,
            "created": "2024-12-15",
            "author": "Admin"
        },
        {
            "id": 2,
            "message": "🚀 New Website Intelligence Hub features now available! Check out the enhanced performance monitoring.",
            "type": "info", 
            "active": True,
            "dismissible": False,
            "created": "2024-12-13",
            "author": "Admin"
        }
    ]

# Initialize demo data
init_demo_data()

# Email sending function (mock)
async def send_email(to_email: str, subject: str, body: str):
    """Mock email sending function"""
    print(f"Sending email to {to_email}: {subject}")
    # In production, integrate with actual email service
    await asyncio.sleep(0.1)  # Simulate email sending delay

# Contact Form Endpoints
@router.post("/contact")
async def submit_contact_form(form: ContactForm, background_tasks: BackgroundTasks):
    """Submit a contact support request"""
    try:
        contact_request = {
            "id": str(uuid.uuid4()),
            "email": form.email,
            "name": form.name or "Anonymous",
            "subject": form.subject or "Support Request",
            "comments": form.comments or "",
            "submitted_at": datetime.now().isoformat(),
            "status": "received"
        }
        
        CONTACT_REQUESTS.append(contact_request)
        
        # Send confirmation email (in background)
        background_tasks.add_task(
            send_email,
            form.email,
            f"Support Request Received - {contact_request['subject']}",
            f"Hi {contact_request['name']},\n\nWe've received your support request and will respond within 24 hours.\n\nBest regards,\nCustomerMind IQ Support Team"
        )
        
        # Notify support team (in background)
        background_tasks.add_task(
            send_email,
            "Support@CustomerMindIQ.com",
            f"New Support Request: {contact_request['subject']}",
            f"New support request from {form.email}:\n\n{form.comments or 'No comments provided'}"
        )
        
        return {
            "success": True,
            "message": "Support request submitted successfully",
            "request_id": contact_request["id"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting contact form: {str(e)}")

@router.get("/contact/requests")
async def get_contact_requests():
    """Get all contact requests (admin only)"""
    try:
        return {
            "success": True,
            "requests": CONTACT_REQUESTS
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving contact requests: {str(e)}")

# Community Posts Endpoints
@router.get("/community/posts")
async def get_community_posts():
    """Get all visible community posts"""
    try:
        visible_posts = [post for post in COMMUNITY_POSTS if post.get("isVisible", True)]
        # Sort by pinned first, then by date
        sorted_posts = sorted(visible_posts, key=lambda x: (not x.get("isPinned", False), x.get("date", "")), reverse=True)
        
        return {
            "success": True,
            "posts": sorted_posts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving community posts: {str(e)}")

@router.post("/community/posts")
async def create_community_post(post: CommunityPost):
    """Create a new community post"""
    try:
        new_post = {
            "id": len(COMMUNITY_POSTS) + 1,
            "title": post.title,
            "content": post.content,
            "type": post.type,
            "author": post.author,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "replies": 0,
            "likes": 0,
            "isPinned": False,
            "isVisible": True
        }
        
        COMMUNITY_POSTS.append(new_post)
        
        return {
            "success": True,
            "message": "Community post created successfully",
            "post": new_post
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating community post: {str(e)}")

@router.put("/community/posts/{post_id}")
async def update_community_post(post_id: int, updates: Dict[str, Any]):
    """Update a community post (admin only)"""
    try:
        post_index = next((i for i, p in enumerate(COMMUNITY_POSTS) if p["id"] == post_id), None)
        
        if post_index is None:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Update the post
        COMMUNITY_POSTS[post_index].update(updates)
        
        return {
            "success": True,
            "message": "Post updated successfully",
            "post": COMMUNITY_POSTS[post_index]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating post: {str(e)}")

@router.delete("/community/posts/{post_id}")
async def delete_community_post(post_id: int):
    """Delete a community post (admin only)"""
    try:
        global COMMUNITY_POSTS
        COMMUNITY_POSTS = [p for p in COMMUNITY_POSTS if p["id"] != post_id]
        
        return {
            "success": True,
            "message": "Post deleted successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting post: {str(e)}")

# Admin Endpoints
@router.get("/admin/announcements")
async def get_announcements():
    """Get all announcements"""
    try:
        return {
            "success": True,
            "announcements": ANNOUNCEMENTS
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving announcements: {str(e)}")

@router.post("/admin/announcements")
async def create_announcement(announcement: Announcement):
    """Create a new announcement (admin only)"""
    try:
        new_announcement = {
            "id": len(ANNOUNCEMENTS) + 1,
            "message": announcement.message,
            "type": announcement.type,
            "active": announcement.active,
            "dismissible": announcement.dismissible,
            "created": datetime.now().strftime("%Y-%m-%d"),
            "author": "Admin"
        }
        
        ANNOUNCEMENTS.append(new_announcement)
        
        return {
            "success": True,
            "message": "Announcement created successfully",
            "announcement": new_announcement
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating announcement: {str(e)}")

@router.put("/admin/announcements/{announcement_id}")
async def update_announcement(announcement_id: int, updates: Dict[str, Any]):
    """Update an announcement (admin only)"""
    try:
        announcement_index = next((i for i, a in enumerate(ANNOUNCEMENTS) if a["id"] == announcement_id), None)
        
        if announcement_index is None:
            raise HTTPException(status_code=404, detail="Announcement not found")
        
        # Update the announcement
        ANNOUNCEMENTS[announcement_index].update(updates)
        
        return {
            "success": True,
            "message": "Announcement updated successfully",
            "announcement": ANNOUNCEMENTS[announcement_index]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating announcement: {str(e)}")

@router.delete("/admin/announcements/{announcement_id}")
async def delete_announcement(announcement_id: int):
    """Delete an announcement (admin only)"""
    try:
        global ANNOUNCEMENTS
        ANNOUNCEMENTS = [a for a in ANNOUNCEMENTS if a["id"] != announcement_id]
        
        return {
            "success": True,
            "message": "Announcement deleted successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting announcement: {str(e)}")

# Dashboard endpoint for admin stats
@router.get("/admin/stats")
async def get_admin_stats():
    """Get admin dashboard statistics"""
    try:
        stats = {
            "total_announcements": len(ANNOUNCEMENTS),
            "active_announcements": len([a for a in ANNOUNCEMENTS if a.get("active", False)]),
            "total_community_posts": len(COMMUNITY_POSTS),
            "pinned_posts": len([p for p in COMMUNITY_POSTS if p.get("isPinned", False)]),
            "total_contact_requests": len(CONTACT_REQUESTS),
            "recent_contact_requests": len([r for r in CONTACT_REQUESTS if r.get("status") == "received"])
        }
        
        return {
            "success": True,
            "stats": stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving admin stats: {str(e)}")

# FAQ endpoint (static for now)
@router.get("/faq")
async def get_faq_data():
    """Get FAQ data"""
    try:
        faq_data = [
            {
                "id": 1,
                "category": "Getting Started",
                "question": "How do I add my first website for monitoring?",
                "answer": "To add your first website, navigate to the Website Intelligence Hub and click the 'Add Website' button. Enter your domain name, website name, and select the type. The system will automatically begin analyzing your site within minutes.",
                "manualRef": "Complete User Guide - Section 3.2: My Websites Tab"
            },
            {
                "id": 2,
                "category": "Performance",
                "question": "What are Core Web Vitals and why do they matter?",
                "answer": "Core Web Vitals are Google's performance metrics that directly affect search rankings: LCP (loading speed), FID (interactivity), and CLS (visual stability). Poor Core Web Vitals can reduce your search visibility and user experience.",
                "manualRef": "Complete User Guide - Section 3.3: Performance Tab"
            },
            # Add more FAQ items...
        ]
        
        return {
            "success": True,
            "faq": faq_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving FAQ data: {str(e)}")