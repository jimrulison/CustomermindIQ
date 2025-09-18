# 🚀 Growth Acceleration Engine - Emergent Deployment Guide

## Step-by-Step Deployment on Emergent

### Phase 1: Prepare for Deployment (You do this)

#### 1. Create New Emergent Project
1. Log into your Emergent dashboard
2. Click **"Create New Project"**
3. Choose **"Full-Stack Application"** (FastAPI + React + MongoDB)
4. Set project name: **"Growth Acceleration Engine"**
5. Set subdomain: **growth.customermindiq.com**

#### 2. Upload Code
1. Zip the `/growth-engine-standalone/` folder I created
2. Upload to your new Emergent project
3. Or copy files manually to your project workspace

#### 3. Configure Environment Variables
In your Emergent project settings, add these environment variables:

**Backend (.env):**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=growth_acceleration_engine
JWT_SECRET=your-super-secret-jwt-key-change-in-production-2025
FRONTEND_URL=https://growth.customermindiq.com
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

**Frontend (.env):**
```env
REACT_APP_API_URL=https://growth.customermindiq.com/api
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

### Phase 2: Stripe Setup (Required for Payments)

#### 1. Create Stripe Account (if you don't have one)
1. Go to https://stripe.com
2. Sign up for account
3. Complete business verification

#### 2. Get API Keys
1. Go to Stripe Dashboard → Developers → API Keys
2. Copy **Publishable key** (starts with `pk_test_`)
3. Copy **Secret key** (starts with `sk_test_`)
4. Add both to environment variables above

#### 3. Create Webhook (for subscription management)
1. Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://growth.customermindiq.com/api/subscription/webhook`
3. Select events: `invoice.payment_succeeded`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted`
4. Copy webhook secret and add to `STRIPE_WEBHOOK_SECRET`

### Phase 3: Deploy and Test

#### 1. Deploy on Emergent
1. Push code to your Emergent project
2. Emergent will automatically:
   - Install backend dependencies from `requirements.txt`
   - Install frontend dependencies from `package.json`
   - Set up MongoDB database
   - Configure subdomain routing

#### 2. Test Deployment
1. Visit: `https://growth.customermindiq.com`
2. Test user registration
3. Test login functionality
4. Test Growth Opportunity Scanner
5. Test subscription flow (with Stripe test cards)

#### 3. Monitor Logs
- Check Emergent logs for any errors
- Verify database connections
- Confirm API endpoints responding

### Phase 4: Go Live

#### 1. Switch to Live Stripe Keys
1. Get live Stripe keys from Stripe Dashboard
2. Update environment variables with live keys
3. Test with real payment methods

#### 2. Launch Marketing
- Update pricing page on main Customer Mind IQ site
- Add links to growth.customermindiq.com
- Announce to existing customers

## 🔧 What I've Already Prepared for You

### ✅ Complete Backend API
- **FastAPI application** with all Growth Engine modules
- **Authentication system** (JWT-based, simple)
- **Subscription management** with Stripe integration
- **Database models** and API endpoints
- **All Growth Engine features**:
  - Growth Opportunity Scanner
  - A/B Testing Engine
  - Revenue Leak Detector
  - ROI Calculator
  - Dashboard with metrics

### ✅ Frontend Structure (Basic)
I haven't created the full React frontend yet, but I can create it based on the existing GrowthAccelerationEngine.js component. Would you like me to create the complete frontend now?

### ✅ Configuration Files
- **Docker setup** (if needed for local development)
- **Environment variable templates**
- **Requirements.txt** with all dependencies
- **README** with full documentation

## 📊 Expected Timeline

### Immediate (Today):
- **You**: Create Emergent project and upload code (30 minutes)
- **You**: Set up Stripe account and get API keys (30 minutes)
- **You**: Configure environment variables (15 minutes)
- **Total**: ~1.5 hours to deploy

### This Week:
- **Me**: Create complete React frontend (if needed)
- **You**: Test all functionality
- **You**: Launch to first customers

### Next Week:
- Monitor usage and feedback
- Iterate based on user needs
- Scale infrastructure if needed

## 💰 Costs Breakdown

### Development: $0 (Already done!)
### Monthly Operational:
- **Emergent hosting**: Your existing rate
- **Stripe fees**: 2.9% + $0.30 per transaction
- **No additional infrastructure costs**

### Revenue Potential:
- **100 customers × $197/month = $19,700/month**
- **1,000 customers × $197/month = $197,000/month**

## 🚨 Next Steps

1. **Create Emergent project** with subdomain growth.customermindiq.com
2. **Get Stripe API keys** for payment processing
3. **Upload the code** I've prepared
4. **Test the deployment**
5. **Let me know if you need the React frontend created**

**Ready to launch your standalone Growth Acceleration Engine! 🚀**

Want me to create the complete React frontend next?