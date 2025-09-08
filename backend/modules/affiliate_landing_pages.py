"""
Affiliate Landing Page Builder System
Allows affiliates to create and customize their own landing pages
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import json
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Database connection
MONGO_URL = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database(os.environ.get('DB_NAME', 'test_database'))

affiliate_pages_router = APIRouter(prefix="/api/affiliate-pages", tags=["Affiliate Landing Pages"])

class AffiliatePageTemplate(BaseModel):
    template_id: str
    name: str
    category: str
    description: str
    preview_image: str
    html_content: str
    css_content: str
    js_content: Optional[str] = ""
    customizable_fields: List[str]

class AffiliatePageData(BaseModel):
    page_id: Optional[str] = None
    affiliate_id: str
    affiliate_number: Optional[str] = None  # Will be auto-generated
    template_id: str
    page_title: str
    page_slug: str
    custom_content: Dict[str, Any]
    is_published: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PageUpdate(BaseModel):
    page_title: Optional[str] = None
    custom_content: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None

# Template configurations with 20 different templates
AFFILIATE_TEMPLATES = [
    {
        "template_id": "saas_modern_1",
        "name": "Modern SaaS Landing",
        "category": "SaaS",
        "description": "Clean, modern design perfect for software products",
        "preview_image": "/templates/previews/saas_modern_1.jpg",
        "customizable_fields": ["headline", "subtitle", "features", "testimonial", "cta_text", "hero_image"]
    },
    {
        "template_id": "saas_minimal_2", 
        "name": "Minimal SaaS Pro",
        "category": "SaaS",
        "description": "Minimalist design focusing on conversions",
        "preview_image": "/templates/previews/saas_minimal_2.jpg",
        "customizable_fields": ["headline", "subtitle", "features", "pricing", "cta_text"]
    },
    {
        "template_id": "saas_enterprise_3",
        "name": "Enterprise SaaS",
        "category": "SaaS",
        "description": "Professional design for B2B software solutions",
        "preview_image": "/templates/previews/saas_enterprise_3.jpg", 
        "customizable_fields": ["headline", "subtitle", "features", "case_studies", "cta_text", "contact_info"]
    },
    {
        "template_id": "saas_startup_4",
        "name": "Startup SaaS",
        "category": "SaaS",
        "description": "Dynamic design perfect for innovative startups",
        "preview_image": "/templates/previews/saas_startup_4.jpg",
        "customizable_fields": ["headline", "subtitle", "features", "team", "cta_text", "social_proof"]
    },
    {
        "template_id": "saas_analytics_5",
        "name": "Analytics SaaS",
        "category": "SaaS", 
        "description": "Data-focused design with charts and metrics",
        "preview_image": "/templates/previews/saas_analytics_5.jpg",
        "customizable_fields": ["headline", "subtitle", "metrics", "features", "dashboard_preview", "cta_text"]
    },
    {
        "template_id": "service_professional_1",
        "name": "Professional Services",
        "category": "Services",
        "description": "Clean design for consulting and professional services",
        "preview_image": "/templates/previews/service_professional_1.jpg",
        "customizable_fields": ["headline", "subtitle", "services", "about", "contact", "cta_text"]
    },
    {
        "template_id": "service_agency_2",
        "name": "Marketing Agency",
        "category": "Services",
        "description": "Creative design perfect for agencies",
        "preview_image": "/templates/previews/service_agency_2.jpg",
        "customizable_fields": ["headline", "subtitle", "portfolio", "team", "contact", "cta_text"]
    },
    {
        "template_id": "service_consulting_3",
        "name": "Business Consulting",
        "category": "Services",
        "description": "Corporate design for consulting firms", 
        "preview_image": "/templates/previews/service_consulting_3.jpg",
        "customizable_fields": ["headline", "subtitle", "expertise", "testimonials", "contact", "cta_text"]
    },
    {
        "template_id": "ecommerce_modern_1",
        "name": "Modern E-commerce",
        "category": "E-commerce",
        "description": "Sleek design for online stores",
        "preview_image": "/templates/previews/ecommerce_modern_1.jpg",
        "customizable_fields": ["headline", "subtitle", "products", "offers", "shipping", "cta_text"]
    },
    {
        "template_id": "ecommerce_fashion_2",
        "name": "Fashion Store",
        "category": "E-commerce",
        "description": "Stylish design for fashion brands",
        "preview_image": "/templates/previews/ecommerce_fashion_2.jpg",
        "customizable_fields": ["headline", "subtitle", "collections", "featured_products", "brand_story", "cta_text"]
    },
    {
        "template_id": "ecommerce_tech_3",
        "name": "Tech Products",
        "category": "E-commerce", 
        "description": "Technical design for gadgets and electronics",
        "preview_image": "/templates/previews/ecommerce_tech_3.jpg",
        "customizable_fields": ["headline", "subtitle", "specifications", "reviews", "warranty", "cta_text"]
    },
    {
        "template_id": "minimal_clean_1",
        "name": "Clean Minimal",
        "category": "Minimal",
        "description": "Ultra-clean design focusing on content",
        "preview_image": "/templates/previews/minimal_clean_1.jpg",
        "customizable_fields": ["headline", "subtitle", "content", "image", "cta_text"]
    },
    {
        "template_id": "minimal_elegant_2",
        "name": "Elegant Minimal",
        "category": "Minimal",
        "description": "Sophisticated minimal design",
        "preview_image": "/templates/previews/minimal_elegant_2.jpg",
        "customizable_fields": ["headline", "subtitle", "content", "quote", "cta_text"]
    },
    {
        "template_id": "minimal_portfolio_3",
        "name": "Portfolio Minimal",
        "category": "Minimal",
        "description": "Clean portfolio showcase",
        "preview_image": "/templates/previews/minimal_portfolio_3.jpg",
        "customizable_fields": ["headline", "subtitle", "portfolio", "about", "contact", "cta_text"]
    },
    {
        "template_id": "bold_creative_1",
        "name": "Bold Creative",
        "category": "Bold",
        "description": "Eye-catching design with bold colors",
        "preview_image": "/templates/previews/bold_creative_1.jpg",
        "customizable_fields": ["headline", "subtitle", "features", "graphics", "testimonial", "cta_text"]
    },
    {
        "template_id": "bold_gradient_2",
        "name": "Gradient Bold",
        "category": "Bold",
        "description": "Modern gradient-based design",
        "preview_image": "/templates/previews/bold_gradient_2.jpg",
        "customizable_fields": ["headline", "subtitle", "benefits", "hero_image", "social_proof", "cta_text"]
    },
    {
        "template_id": "bold_animated_3",
        "name": "Animated Bold",
        "category": "Bold",
        "description": "Dynamic design with animations",
        "preview_image": "/templates/previews/bold_animated_3.jpg",
        "customizable_fields": ["headline", "subtitle", "animations", "features", "testimonial", "cta_text"]
    },
    {
        "template_id": "finance_professional_1",
        "name": "Finance Professional",
        "category": "Industry",
        "description": "Professional design for financial services",
        "preview_image": "/templates/previews/finance_professional_1.jpg",
        "customizable_fields": ["headline", "subtitle", "services", "credentials", "contact", "cta_text"]
    },
    {
        "template_id": "healthcare_modern_1",
        "name": "Healthcare Modern",
        "category": "Industry",
        "description": "Clean design for healthcare providers",
        "preview_image": "/templates/previews/healthcare_modern_1.jpg",
        "customizable_fields": ["headline", "subtitle", "services", "team", "testimonials", "cta_text"]
    },
    {
        "template_id": "education_academic_1",
        "name": "Education Academic",
        "category": "Industry",
        "description": "Academic design for educational content",
        "preview_image": "/templates/previews/education_academic_1.jpg",
        "customizable_fields": ["headline", "subtitle", "courses", "instructors", "testimonials", "cta_text"]
    }
]

@affiliate_pages_router.get("/templates")
async def get_affiliate_templates():
    """Get all available affiliate landing page templates"""
    try:
        return {
            "success": True,
            "templates": AFFILIATE_TEMPLATES,
            "total_templates": len(AFFILIATE_TEMPLATES),
            "categories": list(set([template["category"] for template in AFFILIATE_TEMPLATES])),
            "message": "Affiliate templates retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve templates: {str(e)}")

@affiliate_pages_router.get("/templates/{template_id}")
async def get_template_details(template_id: str):
    """Get detailed template information including HTML/CSS/JS"""
    try:
        # Find template
        template = next((t for t in AFFILIATE_TEMPLATES if t["template_id"] == template_id), None)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Get template content (would be stored in files or database in production)
        template_content = await get_template_content(template_id)
        
        return {
            "success": True,
            "template": {**template, **template_content},
            "message": "Template details retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve template: {str(e)}")

@affiliate_pages_router.post("/create")
async def create_affiliate_page(page_data: AffiliatePageData):
    """Create a new affiliate landing page"""
    try:
        # Generate unique page ID and affiliate number
        page_id = str(uuid.uuid4())
        
        # Generate affiliate number (format: AF + 6 digits)
        existing_pages = await db.affiliate_pages.count_documents({})
        affiliate_number = f"AF{(existing_pages + 1):06d}"
        
        # Create page document
        page_document = {
            "page_id": page_id,
            "affiliate_id": page_data.affiliate_id,
            "affiliate_number": affiliate_number,
            "template_id": page_data.template_id,
            "page_title": page_data.page_title,
            "page_slug": page_data.page_slug.lower().replace(" ", "-"),
            "custom_content": page_data.custom_content,
            "is_published": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "view_count": 0,
            "conversion_count": 0
        }
        
        # Insert into database
        await db.affiliate_pages.insert_one(page_document)
        
        return {
            "success": True,
            "page_id": page_id,
            "affiliate_number": affiliate_number,
            "page_url": f"/affiliate/{affiliate_number}/{page_data.page_slug}",
            "message": "Affiliate landing page created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create page: {str(e)}")

@affiliate_pages_router.get("/affiliate/{affiliate_id}")
async def get_affiliate_pages(affiliate_id: str):
    """Get all pages for a specific affiliate"""
    try:
        pages = await db.affiliate_pages.find(
            {"affiliate_id": affiliate_id}
        ).to_list(length=None)
        
        # Convert ObjectId to string and clean up the data
        for page in pages:
            if '_id' in page:
                del page['_id']  # Remove MongoDB ObjectId
            if 'created_at' in page and page['created_at']:
                page['created_at'] = page['created_at'].isoformat() if hasattr(page['created_at'], 'isoformat') else str(page['created_at'])
            if 'updated_at' in page and page['updated_at']:
                page['updated_at'] = page['updated_at'].isoformat() if hasattr(page['updated_at'], 'isoformat') else str(page['updated_at'])
        
        return {
            "success": True,
            "pages": pages,
            "total_pages": len(pages),
            "message": "Affiliate pages retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve pages: {str(e)}")

@affiliate_pages_router.put("/update/{page_id}")
async def update_affiliate_page(page_id: str, updates: PageUpdate):
    """Update an affiliate landing page"""
    try:
        update_data = {
            "updated_at": datetime.now()
        }
        
        if updates.page_title:
            update_data["page_title"] = updates.page_title
        if updates.custom_content:
            update_data["custom_content"] = updates.custom_content
        if updates.is_published is not None:
            update_data["is_published"] = updates.is_published
        
        result = await db.affiliate_pages.update_one(
            {"page_id": page_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Page not found")
        
        return {
            "success": True,
            "message": "Page updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update page: {str(e)}")

@affiliate_pages_router.get("/render/{affiliate_number}/{page_slug}")
async def render_affiliate_page(affiliate_number: str, page_slug: str):
    """Render the actual affiliate landing page"""
    try:
        # Find the page
        page = await db.affiliate_pages.find_one({
            "affiliate_number": affiliate_number,
            "page_slug": page_slug,
            "is_published": True
        })
        
        if not page:
            raise HTTPException(status_code=404, detail="Page not found or not published")
        
        # Clean up ObjectId
        if '_id' in page:
            del page['_id']
        
        # Increment view count
        await db.affiliate_pages.update_one(
            {"page_id": page["page_id"]},
            {"$inc": {"view_count": 1}}
        )
        
        # Get template content
        template_content = await get_template_content(page["template_id"])
        
        # Merge custom content with template
        rendered_html = await render_template_with_content(
            template_content["html_content"],
            page["custom_content"],
            affiliate_number
        )
        
        return {
            "success": True,
            "html_content": rendered_html,
            "css_content": template_content["css_content"],
            "js_content": template_content["js_content"],
            "page_data": {
                "page_id": page["page_id"],
                "affiliate_number": page["affiliate_number"],
                "page_title": page["page_title"],
                "view_count": page.get("view_count", 0) + 1
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render page: {str(e)}")

@affiliate_pages_router.delete("/delete/{page_id}")
async def delete_affiliate_page(page_id: str):
    """Delete an affiliate landing page"""
    try:
        result = await db.affiliate_pages.delete_one({"page_id": page_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Page not found")
        
        return {
            "success": True,
            "message": "Page deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete page: {str(e)}")

async def get_template_content(template_id: str):
    """Get HTML/CSS/JS content for a template"""
    # This would load from files or database in production
    # For now, returning sample content
    return {
        "html_content": """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{page_title}}</title>
            <style>{{css_content}}</style>
        </head>
        <body>
            <header class="hero">
                <div class="container">
                    <h1>{{headline}}</h1>
                    <p>{{subtitle}}</p>
                    <button class="cta-button">{{cta_text}}</button>
                </div>
            </header>
            <main>
                <section class="features">
                    <div class="container">
                        <h2>Why Choose CustomerMind IQ?</h2>
                        <div class="features-grid">{{features}}</div>
                    </div>
                </section>
                <section class="testimonial">
                    <div class="container">
                        <blockquote>{{testimonial}}</blockquote>
                    </div>
                </section>
            </main>
            <footer>
                <div class="container">
                    <p>Affiliate #{{affiliate_number}} | CustomerMind IQ</p>
                </div>
            </footer>
            <script>{{js_content}}</script>
        </body>
        </html>
        """,
        "css_content": """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 100px 0; text-align: center; }
        .hero h1 { font-size: 3rem; margin-bottom: 20px; }
        .hero p { font-size: 1.2rem; margin-bottom: 30px; }
        .cta-button { background: #ff6b6b; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 1.1rem; cursor: pointer; transition: background 0.3s; }
        .cta-button:hover { background: #ff5252; }
        .features { padding: 80px 0; background: #f8f9fa; }
        .features h2 { text-align: center; margin-bottom: 50px; font-size: 2.5rem; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
        .testimonial { padding: 60px 0; background: white; text-align: center; }
        .testimonial blockquote { font-style: italic; font-size: 1.3rem; color: #666; }
        footer { background: #333; color: white; padding: 40px 0; text-align: center; }
        """,
        "js_content": """
        document.addEventListener('DOMContentLoaded', function() {
            // Track affiliate clicks
            const ctaButtons = document.querySelectorAll('.cta-button');
            ctaButtons.forEach(button => {
                button.addEventListener('click', function() {
                    // Add affiliate tracking logic here
                    window.location.href = 'https://www.customermindiq.com/?ref=' + '{{affiliate_number}}';
                });
            });
        });
        """
    }

async def render_template_with_content(html_template: str, custom_content: dict, affiliate_number: str):
    """Render template with custom content"""
    rendered_html = html_template
    
    # Replace placeholders with custom content
    for key, value in custom_content.items():
        placeholder = f"{{{{{key}}}}}"
        rendered_html = rendered_html.replace(placeholder, str(value))
    
    # Replace affiliate number
    rendered_html = rendered_html.replace("{{affiliate_number}}", affiliate_number)
    
    return rendered_html