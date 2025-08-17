"""
Customer Mind IQ - Customer Profile Manager
Aggregates customer data from all platforms into unified profiles
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from ..connectors.base_connector import UniversalCustomer, UniversalTransaction, UniversalProduct
from .universal_models import UniversalCustomerProfile, CustomerValue, ChurnRisk, PurchaseIntent
import os

class CustomerProfileManager:
    """
    Manages unified customer profiles across all connected platforms
    """
    
    def __init__(self):
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.customer_mind_iq_universal
        
    async def merge_customer_data(self, customers: List[UniversalCustomer], transactions: List[UniversalTransaction]) -> List[UniversalCustomerProfile]:
        """
        Merge customer data from multiple platforms into unified profiles
        """
        try:
            # Group customers by email (primary matching key)
            customer_groups = {}
            
            for customer in customers:
                email = customer.email.lower().strip()
                if not email:
                    continue
                    
                if email not in customer_groups:
                    customer_groups[email] = {
                        'customers': [],
                        'transactions': [],
                        'platforms': set()
                    }
                
                customer_groups[email]['customers'].append(customer)
                customer_groups[email]['platforms'].add(customer.platform_name)
            
            # Group transactions by customer
            for transaction in transactions:
                # Find matching customer group by looking up customer_id
                customer_email = await self._find_customer_email_by_id(transaction.customer_id, customers)
                if customer_email and customer_email in customer_groups:
                    customer_groups[customer_email]['transactions'].append(transaction)
            
            # Create unified profiles
            unified_profiles = []
            for email, group_data in customer_groups.items():
                profile = await self._create_unified_profile(email, group_data)
                unified_profiles.append(profile)
            
            # Store profiles in database
            await self._store_unified_profiles(unified_profiles)
            
            print(f"✅ Created {len(unified_profiles)} unified customer profiles")
            return unified_profiles
            
        except Exception as e:
            print(f"❌ Error merging customer data: {e}")
            return []
    
    async def _find_customer_email_by_id(self, customer_id: str, customers: List[UniversalCustomer]) -> Optional[str]:
        """Find customer email by universal customer ID"""
        for customer in customers:
            if customer.customer_id == customer_id:
                return customer.email.lower().strip()
        return None
    
    async def _create_unified_profile(self, email: str, group_data: Dict) -> UniversalCustomerProfile:
        """Create a unified customer profile from grouped data"""
        customers = group_data['customers']
        transactions = group_data['transactions']
        platforms = list(group_data['platforms'])
        
        # Aggregate basic info (take from most recent or most complete)
        primary_customer = max(customers, key=lambda c: c.total_spent if c.total_spent else 0)
        
        # Aggregate spending across all platforms
        total_spent = sum(c.total_spent for c in customers if c.total_spent)
        total_orders = sum(c.total_orders for c in customers if c.total_orders)
        
        # Find first seen and last activity dates
        first_seen = min((c.created_date for c in customers if c.created_date), default=datetime.now())
        last_activity = max((c.last_order_date for c in customers if c.last_order_date), default=None)
        
        # Calculate behavioral scores
        purchase_frequency_score = await self._calculate_purchase_frequency_score(total_orders, first_seen)
        engagement_score = await self._calculate_engagement_score(customers, transactions)
        loyalty_score = await self._calculate_loyalty_score(len(platforms), total_spent, first_seen)
        
        # Determine customer tiers
        customer_value_tier = await self._determine_value_tier(total_spent, total_orders)
        churn_risk_level = await self._determine_churn_risk(last_activity, engagement_score)
        purchase_intent = await self._determine_purchase_intent(transactions, engagement_score)
        
        # Create platform-specific data
        platform_data = {}
        for customer in customers:
            platform_data[customer.platform_name] = {
                'customer_id': customer.customer_id,
                'platform_customer_id': customer.platform_customer_id,
                'total_spent': customer.total_spent,
                'total_orders': customer.total_orders,
                'last_order_date': customer.last_order_date,
                'status': customer.status,
                'metadata': customer.metadata
            }
        
        # Generate AI insights
        behavioral_patterns = await self._analyze_behavioral_patterns(customers, transactions)
        predicted_actions = await self._predict_customer_actions(customer_value_tier, churn_risk_level, purchase_intent)
        recommended_strategies = await self._recommend_strategies(customer_value_tier, churn_risk_level, platforms)
        
        # Create unified profile
        unified_profile = UniversalCustomerProfile(
            customer_id=f"unified_{hash(email)}",
            email=email,
            name=primary_customer.name,
            total_spent_all_platforms=total_spent,
            total_orders_all_platforms=total_orders,
            platforms_active=platforms,
            first_seen_date=first_seen,
            last_activity_date=last_activity,
            customer_value_tier=customer_value_tier,
            churn_risk_level=churn_risk_level,
            purchase_intent=purchase_intent,
            purchase_frequency_score=purchase_frequency_score,
            engagement_score=engagement_score,
            loyalty_score=loyalty_score,
            platform_data=platform_data,
            behavioral_patterns=behavioral_patterns,
            predicted_actions=predicted_actions,
            recommended_strategies=recommended_strategies
        )
        
        return unified_profile
    
    async def _calculate_purchase_frequency_score(self, total_orders: int, first_seen: datetime) -> int:
        """Calculate purchase frequency score (0-100)"""
        if not first_seen:
            return 50
        
        days_active = (datetime.now() - first_seen).days
        if days_active == 0:
            return 50
        
        # Calculate orders per month
        orders_per_month = (total_orders / days_active) * 30
        
        # Score based on frequency (adjust these thresholds as needed)
        if orders_per_month >= 2:
            return 100
        elif orders_per_month >= 1:
            return 80
        elif orders_per_month >= 0.5:
            return 60
        elif orders_per_month >= 0.25:
            return 40
        else:
            return 20
    
    async def _calculate_engagement_score(self, customers: List[UniversalCustomer], transactions: List[UniversalTransaction]) -> int:
        """Calculate overall engagement score (0-100)"""
        # Base score from customer data
        base_score = sum(c.metadata.get('engagement_score', 50) for c in customers) / len(customers) if customers else 50
        
        # Adjust based on recent transaction activity
        recent_transactions = [t for t in transactions if t.transaction_date > datetime.now() - timedelta(days=30)]
        recent_activity_boost = min(len(recent_transactions) * 10, 30)
        
        # Adjust based on platform diversity (more platforms = higher engagement)
        platform_diversity_boost = len(set(c.platform_name for c in customers)) * 5
        
        final_score = min(int(base_score + recent_activity_boost + platform_diversity_boost), 100)
        return max(final_score, 0)
    
    async def _calculate_loyalty_score(self, platform_count: int, total_spent: float, first_seen: datetime) -> int:
        """Calculate customer loyalty score (0-100)"""
        score = 50  # Base score
        
        # Platform diversity bonus
        score += min(platform_count * 15, 30)
        
        # Spending tier bonus
        if total_spent > 10000:
            score += 30
        elif total_spent > 5000:
            score += 20
        elif total_spent > 1000:
            score += 10
        
        # Tenure bonus
        if first_seen:
            days_active = (datetime.now() - first_seen).days
            if days_active > 365:
                score += 20
            elif days_active > 180:
                score += 10
        
        return min(max(score, 0), 100)
    
    async def _determine_value_tier(self, total_spent: float, total_orders: int) -> CustomerValue:
        """Determine customer value tier"""
        if total_spent > 20000 or total_orders > 50:
            return CustomerValue.VIP
        elif total_spent > 10000 or total_orders > 20:
            return CustomerValue.HIGH
        elif total_spent > 2000 or total_orders > 5:
            return CustomerValue.MEDIUM
        else:
            return CustomerValue.LOW
    
    async def _determine_churn_risk(self, last_activity: Optional[datetime], engagement_score: int) -> ChurnRisk:
        """Determine churn risk level"""
        if not last_activity:
            return ChurnRisk.HIGH
        
        days_since_activity = (datetime.now() - last_activity).days
        
        if days_since_activity > 365 or engagement_score < 30:
            return ChurnRisk.CRITICAL
        elif days_since_activity > 180 or engagement_score < 50:
            return ChurnRisk.HIGH
        elif days_since_activity > 90 or engagement_score < 70:
            return ChurnRisk.MEDIUM
        else:
            return ChurnRisk.LOW
    
    async def _determine_purchase_intent(self, transactions: List[UniversalTransaction], engagement_score: int) -> PurchaseIntent:
        """Determine purchase intent level"""
        recent_transactions = [t for t in transactions if t.transaction_date > datetime.now() - timedelta(days=30)]
        
        if len(recent_transactions) > 2 and engagement_score > 80:
            return PurchaseIntent.READY
        elif len(recent_transactions) > 0 and engagement_score > 60:
            return PurchaseIntent.HOT
        elif engagement_score > 40:
            return PurchaseIntent.WARM
        else:
            return PurchaseIntent.COLD
    
    async def _analyze_behavioral_patterns(self, customers: List[UniversalCustomer], transactions: List[UniversalTransaction]) -> List[str]:
        """Analyze customer behavioral patterns"""
        patterns = []
        
        # Multi-platform user
        if len(set(c.platform_name for c in customers)) > 1:
            patterns.append("Multi-platform user")
        
        # High spender
        total_spent = sum(c.total_spent for c in customers if c.total_spent)
        if total_spent > 10000:
            patterns.append("High-value customer")
        elif total_spent > 5000:
            patterns.append("Premium customer")
        
        # Frequent buyer
        total_orders = sum(c.total_orders for c in customers if c.total_orders)
        if total_orders > 20:
            patterns.append("Frequent buyer")
        elif total_orders > 10:
            patterns.append("Regular customer")
        
        # Recent activity
        recent_transactions = [t for t in transactions if t.transaction_date > datetime.now() - timedelta(days=30)]
        if len(recent_transactions) > 2:
            patterns.append("Highly active")
        elif len(recent_transactions) > 0:
            patterns.append("Recently active")
        
        # Consistent spender
        if len(transactions) > 5:
            amounts = [t.amount for t in transactions]
            avg_amount = sum(amounts) / len(amounts)
            consistent_transactions = [t for t in transactions if abs(t.amount - avg_amount) < avg_amount * 0.3]
            if len(consistent_transactions) > len(transactions) * 0.7:
                patterns.append("Consistent spender")
        
        return patterns[:5]  # Return top 5 patterns
    
    async def _predict_customer_actions(self, value_tier: CustomerValue, churn_risk: ChurnRisk, purchase_intent: PurchaseIntent) -> List[str]:
        """Predict likely customer actions"""
        predictions = []
        
        if purchase_intent == PurchaseIntent.READY:
            predictions.append("Likely to make purchase within 7 days")
        elif purchase_intent == PurchaseIntent.HOT:
            predictions.append("Likely to make purchase within 30 days")
        
        if churn_risk == ChurnRisk.CRITICAL:
            predictions.append("At risk of churning within 30 days")
        elif churn_risk == ChurnRisk.HIGH:
            predictions.append("May reduce activity in next 60 days")
        
        if value_tier in [CustomerValue.HIGH, CustomerValue.VIP]:
            predictions.append("Good candidate for premium offerings")
            predictions.append("Likely to respond to personalized outreach")
        
        if value_tier == CustomerValue.LOW and purchase_intent in [PurchaseIntent.WARM, PurchaseIntent.HOT]:
            predictions.append("Growth potential - ready for upselling")
        
        return predictions[:3]  # Return top 3 predictions
    
    async def _recommend_strategies(self, value_tier: CustomerValue, churn_risk: ChurnRisk, platforms: List[str]) -> List[str]:
        """Recommend customer engagement strategies"""
        strategies = []
        
        # Churn prevention strategies
        if churn_risk in [ChurnRisk.HIGH, ChurnRisk.CRITICAL]:
            strategies.append("Immediate retention campaign")
            strategies.append("Personal outreach from account manager")
            strategies.append("Special retention offer or discount")
        
        # Value-based strategies
        if value_tier == CustomerValue.VIP:
            strategies.append("VIP treatment and exclusive access")
            strategies.append("Dedicated customer success manager")
        elif value_tier == CustomerValue.HIGH:
            strategies.append("Premium feature recommendations")
            strategies.append("Loyalty rewards program")
        
        # Growth strategies
        if value_tier in [CustomerValue.LOW, CustomerValue.MEDIUM]:
            strategies.append("Educational content and tutorials")
            strategies.append("Feature adoption campaigns")
        
        # Multi-platform strategies
        if len(platforms) > 1:
            strategies.append("Cross-platform usage optimization")
            strategies.append("Integrated workflow recommendations")
        
        return strategies[:4]  # Return top 4 strategies
    
    async def _store_unified_profiles(self, profiles: List[UniversalCustomerProfile]):
        """Store unified profiles in database"""
        try:
            documents = [profile.dict() for profile in profiles]
            
            # Upsert profiles (update if exists, insert if new)
            for doc in documents:
                await self.db.unified_customer_profiles.update_one(
                    {"email": doc["email"]},
                    {"$set": doc},
                    upsert=True
                )
            
            print(f"✅ Stored {len(documents)} unified customer profiles")
            
        except Exception as e:
            print(f"❌ Error storing unified profiles: {e}")
    
    async def get_unified_profiles(self, limit: int = 100) -> List[UniversalCustomerProfile]:
        """Retrieve unified customer profiles from database"""
        try:
            cursor = self.db.unified_customer_profiles.find().limit(limit)
            documents = await cursor.to_list(length=limit)
            
            profiles = []
            for doc in documents:
                # Convert datetime strings back to datetime objects
                if isinstance(doc.get('first_seen_date'), str):
                    doc['first_seen_date'] = datetime.fromisoformat(doc['first_seen_date'].replace('Z', '+00:00'))
                if isinstance(doc.get('last_activity_date'), str):
                    doc['last_activity_date'] = datetime.fromisoformat(doc['last_activity_date'].replace('Z', '+00:00'))
                if isinstance(doc.get('created_at'), str):
                    doc['created_at'] = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
                if isinstance(doc.get('last_updated'), str):
                    doc['last_updated'] = datetime.fromisoformat(doc['last_updated'].replace('Z', '+00:00'))
                
                profile = UniversalCustomerProfile(**doc)
                profiles.append(profile)
            
            return profiles
            
        except Exception as e:
            print(f"❌ Error retrieving unified profiles: {e}")
            return []
    
    async def get_profile_by_email(self, email: str) -> Optional[UniversalCustomerProfile]:
        """Get unified profile by email"""
        try:
            doc = await self.db.unified_customer_profiles.find_one({"email": email.lower()})
            if doc:
                return UniversalCustomerProfile(**doc)
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving profile by email: {e}")
            return None