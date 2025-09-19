"""
Growth Acceleration Engine - Standalone Website
Domain: GrowthAccelerationEngine.com
AI-powered growth opportunity identification, A/B testing, and revenue optimization
"""

import os
import asyncio
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Growth Engine modules
from routers.auth import auth_router
from routers.subscription import subscription_router
from routers.growth_engine import growth_engine_router
from routers.dashboard import dashboard_router

# Environment variables
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "growth_acceleration_engine")
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://growthaccelerationengine.com")

# Database client
mongo_client = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global mongo_client, db
    try:
        mongo_client = AsyncIOMotorClient(MONGO_URL)
        db = mongo_client[DB_NAME]
        
        # Test connection
        await mongo_client.admin.command('ping')
        logger.info(f"✅ Connected to MongoDB: {DB_NAME}")
        
        # Create indexes
        await create_indexes()
        
        yield
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise
    finally:
        # Shutdown
        if mongo_client:
            mongo_client.close()
            logger.info("📴 Database connection closed")

async def create_indexes():
    """Create database indexes for performance"""
    try:
        # Users collection indexes
        await db.users.create_index("email", unique=True)
        await db.users.create_index("created_at")
        
        # Growth data indexes
        await db.growth_opportunities.create_index("user_email")
        await db.growth_opportunities.create_index("created_at")
        await db.ab_tests.create_index("user_email")
        await db.revenue_leaks.create_index("user_email")
        await db.roi_calculations.create_index("user_email")
        
        logger.info("✅ Database indexes created")
    except Exception as e:
        logger.error(f"❌ Index creation failed: {e}")

# Create FastAPI app
app = FastAPI(
    title="Growth Acceleration Engine",
    description="AI-powered growth opportunity identification, A/B testing, and revenue optimization platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL, 
        "https://growthaccelerationengine.com",
        "https://www.growthaccelerationengine.com",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make database accessible to routers
@app.middleware("http")
async def add_db_to_request(request, call_next):
    request.state.db = db
    response = await call_next(request)
    return response

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        await mongo_client.admin.command('ping')
        return {
            "status": "healthy",
            "service": "Growth Acceleration Engine",
            "domain": "GrowthAccelerationEngine.com",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Growth Acceleration Engine API",
        "domain": "GrowthAccelerationEngine.com",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/health"
    }

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(subscription_router, prefix="/api/subscription", tags=["Subscription"])
app.include_router(growth_engine_router, prefix="/api/growth", tags=["Growth Engine"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )