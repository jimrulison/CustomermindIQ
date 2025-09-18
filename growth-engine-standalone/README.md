# Growth Acceleration Engine - Standalone

AI-powered growth opportunity identification, A/B testing, and revenue optimization platform.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Local Development

1. **Clone and Setup**
```bash
cd growth-engine-standalone
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

2. **Start with Docker Compose**
```bash
docker-compose up -d
```

3. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup (Without Docker)

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env file with your configuration
uvicorn main:app --reload
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

3. **Database Setup**
- Install MongoDB locally or use MongoDB Atlas
- Update MONGO_URL in backend/.env

## 🔧 Configuration

### Backend Environment Variables (.env)
```env
# Database
MONGO_URL=mongodb://localhost:27017
DB_NAME=growth_acceleration_engine

# Security
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# Frontend URL
FRONTEND_URL=https://growth.customermindiq.com

# Stripe (for payments)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

### Frontend Environment Variables (.env)
```env
REACT_APP_API_URL=https://growth.customermindiq.com/api
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
```

## 📊 Features

### Core Modules
- **Growth Opportunity Scanner**: AI-powered growth identification
- **A/B Testing Engine**: Automated testing and optimization
- **Revenue Leak Detector**: Identify and fix revenue losses
- **ROI Calculator**: Investment analysis and projections
- **Dashboard**: Unified growth metrics and insights

### Authentication
- JWT-based authentication
- User registration and login
- Password reset functionality

### Subscription Management
- Multiple pricing tiers
- Stripe integration for payments
- Subscription status tracking

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── main.py                 # FastAPI application
├── routers/               # API endpoints
│   ├── auth.py           # Authentication
│   ├── subscription.py   # Billing/subscriptions
│   ├── growth_opportunity_scanner.py
│   ├── automated_ab_testing.py
│   ├── revenue_leak_detector.py
│   ├── roi_calculator.py
│   └── growth_engine_dashboard.py
└── requirements.txt
```

### Frontend (React)
```
frontend/
├── src/
│   ├── components/       # React components
│   ├── pages/           # Page components
│   ├── hooks/           # Custom hooks
│   ├── utils/           # Utilities
│   └── App.js           # Main app
├── public/
└── package.json
```

## 🚀 Deployment

### Emergent Platform (Recommended)
1. Create new project on Emergent
2. Set subdomain: growth.customermindiq.com
3. Deploy backend and frontend separately
4. Configure environment variables

### Manual Deployment
1. **Backend**: Deploy to any cloud provider (AWS, DigitalOcean, etc.)
2. **Frontend**: Deploy to Vercel, Netlify, or CDN
3. **Database**: MongoDB Atlas or self-hosted
4. **Domain**: Configure DNS for subdomain

## 💰 Pricing Configuration

Current pricing tiers:
- **Growth Starter**: $97/month
- **Growth Professional**: $197/month (Most Popular)
- **Growth Enterprise**: $397/month

Update pricing in `backend/routers/subscription.py`

## 🔗 API Documentation

Access interactive API docs at: `http://localhost:8000/docs`

### Key Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/growth/scan` - Scan growth opportunities
- `POST /api/ab-testing/create` - Create A/B test
- `POST /api/revenue/scan` - Detect revenue leaks
- `POST /api/roi/calculate` - Calculate ROI

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📈 Monitoring

- Health check: `GET /health`
- Metrics dashboard in frontend
- Database monitoring via MongoDB tools

## 🛡️ Security

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- Input validation with Pydantic
- Environment variable configuration

## 🤝 Support

For support and questions:
- Email: info@FancyFreeLiving.com
- Documentation: Available in `/docs` endpoint

## 📄 License

Copyright (c) 2025 Fancy Free Living LLC. All rights reserved.