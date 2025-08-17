"""
Customer Mind IQ - Sentiment Analysis Microservice
AI-powered customer sentiment analysis and emotional intelligence
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import uuid

class SentimentProfile(BaseModel):
    customer_id: str
    overall_sentiment: float  # -1 to 1 (negative to positive)
    sentiment_label: str  # very_negative, negative, neutral, positive, very_positive
    confidence_score: float  # 0 to 1
    emotion_breakdown: Dict[str, float]  # joy, anger, fear, sadness, surprise, trust
    sentiment_trend: str  # improving, declining, stable
    key_sentiment_drivers: List[str]
    satisfaction_indicators: Dict[str, Any]
    risk_alerts: List[str]
    engagement_recommendations: List[str]

class SentimentInsight(BaseModel):
    insight_id: str
    customer_id: str
    source: str  # email, support_ticket, survey, review
    text_sample: str
    sentiment_score: float
    emotions_detected: List[str]
    topics_mentioned: List[str]
    urgency_level: str  # low, medium, high, critical
    suggested_response: str

class SentimentAnalysisService:
    """Customer Mind IQ Sentiment Analysis Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.customer_mind_iq
    
    async def analyze_customer_sentiment(self, customers_data: List[Dict]) -> List[SentimentProfile]:
        """Analyze sentiment for all customers using AI"""
        try:
            sentiment_profiles = []
            
            for customer in customers_data:
                profile = await self._analyze_individual_sentiment(customer)
                sentiment_profiles.append(profile)
            
            # Store results
            await self._store_sentiment_results(sentiment_profiles)
            
            return sentiment_profiles
            
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return await self._fallback_sentiment_analysis(customers_data)
    
    async def _analyze_individual_sentiment(self, customer: Dict) -> SentimentProfile:
        """Analyze sentiment for individual customer using AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"sentiment_analysis_{customer.get('customer_id', 'unknown')}",
                system_message="""You are Customer Mind IQ's sentiment analysis specialist. Analyze customer data 
                to understand emotional state, satisfaction levels, and engagement sentiment for software customers."""
            ).with_model("openai", "gpt-4o-mini")
            
            # Gather customer behavioral indicators for sentiment analysis
            behavioral_indicators = {
                "engagement_score": customer.get('engagement_score', 50),
                "purchase_frequency": customer.get('total_purchases', 0),
                "spending_trend": self._calculate_spending_trend(customer),
                "lifecycle_stage": customer.get('lifecycle_stage', 'unknown'),
                "software_adoption": len(customer.get('software_owned', [])),
                "last_interaction": self._days_since_last_purchase(customer.get('last_purchase_date')),
                "purchase_patterns": customer.get('purchase_patterns', {})
            }
            
            sentiment_prompt = f"""
            Analyze customer sentiment using Customer Mind IQ emotional intelligence algorithms:
            
            Customer Profile:
            - ID: {customer.get('customer_id')}
            - Name: {customer.get('name')}
            - Email: {customer.get('email')}
            - Behavioral Indicators: {json.dumps(behavioral_indicators, default=str)}
            - Software Portfolio: {customer.get('software_owned', [])}
            
            Analyze sentiment considering:
            1. Purchase behavior patterns and frequency
            2. Engagement levels and interaction quality
            3. Software adoption and usage patterns
            4. Customer lifecycle position and progression
            5. Communication responsiveness indicators
            
            Provide comprehensive sentiment analysis in this exact JSON format:
            {{
                "overall_sentiment": <-1.0 to 1.0>,
                "sentiment_label": "<very_negative/negative/neutral/positive/very_positive>",
                "confidence_score": <0.0 to 1.0>,
                "emotion_breakdown": {{
                    "satisfaction": <0.0 to 1.0>,
                    "enthusiasm": <0.0 to 1.0>,
                    "trust": <0.0 to 1.0>,
                    "frustration": <0.0 to 1.0>,
                    "loyalty": <0.0 to 1.0>,
                    "engagement": <0.0 to 1.0>
                }},
                "sentiment_trend": "<improving/declining/stable>",
                "key_sentiment_drivers": ["driver1", "driver2", "driver3"],
                "satisfaction_indicators": {{
                    "product_satisfaction": <0.0 to 1.0>,
                    "service_satisfaction": <0.0 to 1.0>,
                    "value_perception": <0.0 to 1.0>,
                    "recommendation_likelihood": <0.0 to 1.0>
                }},
                "risk_alerts": ["alert1", "alert2"],
                "engagement_recommendations": ["recommendation1", "recommendation2", "recommendation3"]
            }}
            
            Base analysis on concrete behavioral data and customer interaction patterns.
            """
            
            message = UserMessage(text=sentiment_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                
                return SentimentProfile(
                    customer_id=customer['customer_id'],
                    overall_sentiment=analysis.get('overall_sentiment', 0.0),
                    sentiment_label=analysis.get('sentiment_label', 'neutral'),
                    confidence_score=analysis.get('confidence_score', 0.7),
                    emotion_breakdown=analysis.get('emotion_breakdown', {}),
                    sentiment_trend=analysis.get('sentiment_trend', 'stable'),
                    key_sentiment_drivers=analysis.get('key_sentiment_drivers', []),
                    satisfaction_indicators=analysis.get('satisfaction_indicators', {}),
                    risk_alerts=analysis.get('risk_alerts', []),
                    engagement_recommendations=analysis.get('engagement_recommendations', [])
                )
                
            except json.JSONDecodeError:
                return await self._fallback_individual_sentiment(customer)
                
        except Exception as e:
            print(f"Individual sentiment analysis error: {e}")
            return await self._fallback_individual_sentiment(customer)
    
    async def analyze_sentiment_from_text(self, customer_id: str, text: str, source: str) -> SentimentInsight:
        """Analyze sentiment from specific customer text/communication"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"text_sentiment_{customer_id}_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's text sentiment analyzer. Analyze specific customer 
                communications to extract emotional intelligence and provide actionable insights."""
            ).with_model("openai", "gpt-4o-mini")
            
            text_analysis_prompt = f"""
            Analyze sentiment from this customer communication:
            
            Source: {source}
            Customer ID: {customer_id}
            Text: "{text}"
            
            Provide detailed text sentiment analysis in JSON format:
            {{
                "sentiment_score": <-1.0 to 1.0>,
                "emotions_detected": ["emotion1", "emotion2"],
                "topics_mentioned": ["topic1", "topic2"],
                "urgency_level": "<low/medium/high/critical>",
                "suggested_response": "<professional response suggestion>",
                "key_phrases": ["phrase1", "phrase2"],
                "concern_areas": ["concern1", "concern2"]
            }}
            
            Focus on:
            1. Emotional tone and intensity
            2. Specific software-related concerns or praise
            3. Urgency indicators
            4. Topics requiring attention
            5. Appropriate response strategy
            """
            
            message = UserMessage(text=text_analysis_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                
                return SentimentInsight(
                    insight_id=str(uuid.uuid4()),
                    customer_id=customer_id,
                    source=source,
                    text_sample=text[:200] + "..." if len(text) > 200 else text,
                    sentiment_score=analysis.get('sentiment_score', 0.0),
                    emotions_detected=analysis.get('emotions_detected', []),
                    topics_mentioned=analysis.get('topics_mentioned', []),
                    urgency_level=analysis.get('urgency_level', 'medium'),
                    suggested_response=analysis.get('suggested_response', 'Thank you for your feedback.')
                )
                
            except json.JSONDecodeError:
                return self._fallback_text_sentiment(customer_id, text, source)
                
        except Exception as e:
            print(f"Text sentiment analysis error: {e}")
            return self._fallback_text_sentiment(customer_id, text, source)
    
    async def get_sentiment_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive sentiment dashboard analytics"""
        try:
            # Get latest sentiment analysis
            latest_analysis = await self.db.sentiment_analysis.find_one(
                {}, sort=[("created_at", -1)]
            )
            
            if not latest_analysis:
                return await self._generate_sample_sentiment_dashboard()
            
            profiles = latest_analysis.get('profiles', [])
            
            # Calculate sentiment distribution
            sentiment_distribution = {
                "very_positive": 0, "positive": 0, "neutral": 0, "negative": 0, "very_negative": 0
            }
            
            total_customers = len(profiles)
            sentiment_sum = 0
            high_risk_customers = []
            positive_advocates = []
            
            for profile in profiles:
                sentiment_label = profile.get('sentiment_label', 'neutral')
                sentiment_distribution[sentiment_label] += 1
                
                overall_sentiment = profile.get('overall_sentiment', 0.0)
                sentiment_sum += overall_sentiment
                
                # Identify high-risk customers (negative sentiment)
                if overall_sentiment < -0.3:
                    high_risk_customers.append(profile.get('customer_id'))
                
                # Identify positive advocates
                if overall_sentiment > 0.6:
                    positive_advocates.append(profile.get('customer_id'))
            
            avg_sentiment = sentiment_sum / max(total_customers, 1)
            
            # Get most common sentiment drivers
            all_drivers = []
            for profile in profiles:
                all_drivers.extend(profile.get('key_sentiment_drivers', []))
            
            driver_counts = {}
            for driver in all_drivers:
                driver_counts[driver] = driver_counts.get(driver, 0) + 1
            
            top_drivers = sorted(driver_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Calculate satisfaction metrics
            satisfaction_scores = {
                "product_satisfaction": 0,
                "service_satisfaction": 0,
                "value_perception": 0,
                "recommendation_likelihood": 0
            }
            
            for profile in profiles:
                satisfaction_indicators = profile.get('satisfaction_indicators', {})
                for key in satisfaction_scores.keys():
                    satisfaction_scores[key] += satisfaction_indicators.get(key, 0.5)
            
            for key in satisfaction_scores.keys():
                satisfaction_scores[key] = satisfaction_scores[key] / max(total_customers, 1)
            
            return {
                "sentiment_overview": {
                    "total_customers_analyzed": total_customers,
                    "average_sentiment": avg_sentiment,
                    "positive_customers": sentiment_distribution["very_positive"] + sentiment_distribution["positive"],
                    "neutral_customers": sentiment_distribution["neutral"],
                    "negative_customers": sentiment_distribution["negative"] + sentiment_distribution["very_negative"],
                    "high_risk_count": len(high_risk_customers),
                    "advocate_count": len(positive_advocates)
                },
                "sentiment_distribution": sentiment_distribution,
                "satisfaction_metrics": satisfaction_scores,
                "top_sentiment_drivers": [{"driver": driver, "count": count} for driver, count in top_drivers],
                "risk_alerts": {
                    "high_risk_customers": high_risk_customers[:10],  # Top 10 for dashboard
                    "trending_concerns": await self._get_trending_concerns(profiles),
                    "urgent_interventions": len([p for p in profiles if len(p.get('risk_alerts', [])) > 2])
                },
                "opportunities": {
                    "positive_advocates": positive_advocates[:10],  # Top 10 for dashboard
                    "improvement_areas": await self._get_improvement_opportunities(profiles),
                    "engagement_boost_potential": len([p for p in profiles if p.get('overall_sentiment', 0) > -0.2 and p.get('overall_sentiment', 0) < 0.3])
                }
            }
            
        except Exception as e:
            print(f"Sentiment dashboard error: {e}")
            return await self._generate_sample_sentiment_dashboard()
    
    async def _get_trending_concerns(self, profiles: List[Dict]) -> List[str]:
        """Extract trending concerns from sentiment profiles"""
        all_alerts = []
        for profile in profiles:
            all_alerts.extend(profile.get('risk_alerts', []))
        
        alert_counts = {}
        for alert in all_alerts:
            alert_counts[alert] = alert_counts.get(alert, 0) + 1
        
        return [alert for alert, count in sorted(alert_counts.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    async def _get_improvement_opportunities(self, profiles: List[Dict]) -> List[str]:
        """Extract improvement opportunities from sentiment data"""
        opportunities = []
        
        # Count customers by sentiment trend
        declining_count = len([p for p in profiles if p.get('sentiment_trend') == 'declining'])
        stable_count = len([p for p in profiles if p.get('sentiment_trend') == 'stable'])
        
        if declining_count > len(profiles) * 0.2:
            opportunities.append("Address declining sentiment trends")
        
        if stable_count > len(profiles) * 0.6:
            opportunities.append("Activate neutral customers for positive engagement")
        
        # Analyze satisfaction indicators
        low_satisfaction_areas = []
        for profile in profiles:
            satisfaction = profile.get('satisfaction_indicators', {})
            for area, score in satisfaction.items():
                if score < 0.6:
                    low_satisfaction_areas.append(area)
        
        if low_satisfaction_areas:
            most_common_issue = max(set(low_satisfaction_areas), key=low_satisfaction_areas.count)
            opportunities.append(f"Improve {most_common_issue.replace('_', ' ')}")
        
        return opportunities[:3]
    
    def _calculate_spending_trend(self, customer: Dict) -> str:
        """Calculate customer spending trend"""
        total_spent = customer.get('total_spent', 0)
        total_purchases = customer.get('total_purchases', 0)
        
        if total_purchases == 0:
            return "no_history"
        
        avg_per_purchase = total_spent / total_purchases
        
        if avg_per_purchase > 5000:
            return "increasing"
        elif avg_per_purchase > 2000:
            return "stable"
        else:
            return "declining"
    
    def _days_since_last_purchase(self, last_purchase_date) -> int:
        """Calculate days since last purchase"""
        if not last_purchase_date:
            return 365
        
        if isinstance(last_purchase_date, str):
            try:
                last_purchase_date = datetime.fromisoformat(last_purchase_date.replace('Z', '+00:00'))
            except:
                return 365
        
        return (datetime.now() - last_purchase_date).days
    
    async def _fallback_sentiment_analysis(self, customers_data: List[Dict]) -> List[SentimentProfile]:
        """Fallback sentiment analysis when AI fails"""
        profiles = []
        for customer in customers_data:
            profile = await self._fallback_individual_sentiment(customer)
            profiles.append(profile)
        return profiles
    
    async def _fallback_individual_sentiment(self, customer: Dict) -> SentimentProfile:
        """Create fallback sentiment profile"""
        # Rule-based sentiment calculation
        engagement_score = customer.get('engagement_score', 50)
        days_since_purchase = self._days_since_last_purchase(customer.get('last_purchase_date'))
        total_purchases = customer.get('total_purchases', 0)
        
        # Calculate sentiment based on engagement and recency
        base_sentiment = (engagement_score - 50) / 50  # Scale to -1 to 1
        
        if days_since_purchase > 180:
            base_sentiment -= 0.3
        elif days_since_purchase < 30:
            base_sentiment += 0.2
        
        if total_purchases > 5:
            base_sentiment += 0.2
        elif total_purchases == 0:
            base_sentiment -= 0.2
        
        overall_sentiment = max(-1, min(1, base_sentiment))
        
        # Determine sentiment label
        if overall_sentiment >= 0.6:
            sentiment_label = "very_positive"
        elif overall_sentiment >= 0.2:
            sentiment_label = "positive"
        elif overall_sentiment >= -0.2:
            sentiment_label = "neutral"
        elif overall_sentiment >= -0.6:
            sentiment_label = "negative"
        else:
            sentiment_label = "very_negative"
        
        return SentimentProfile(
            customer_id=customer['customer_id'],
            overall_sentiment=overall_sentiment,
            sentiment_label=sentiment_label,
            confidence_score=0.7,
            emotion_breakdown={
                "satisfaction": max(0, overall_sentiment + 0.5),
                "enthusiasm": max(0, overall_sentiment),
                "trust": max(0, overall_sentiment + 0.3),
                "frustration": max(0, -overall_sentiment),
                "loyalty": max(0, overall_sentiment + 0.4),
                "engagement": engagement_score / 100
            },
            sentiment_trend="stable" if abs(overall_sentiment) < 0.3 else "declining" if overall_sentiment < 0 else "improving",
            key_sentiment_drivers=["Purchase behavior", "Engagement patterns", "Communication responsiveness"],
            satisfaction_indicators={
                "product_satisfaction": max(0, overall_sentiment + 0.5),
                "service_satisfaction": 0.6,
                "value_perception": max(0, overall_sentiment + 0.4),
                "recommendation_likelihood": max(0, overall_sentiment + 0.3)
            },
            risk_alerts=["Low engagement"] if engagement_score < 40 else [],
            engagement_recommendations=["Personalized outreach", "Value demonstration", "Feedback collection"]
        )
    
    def _fallback_text_sentiment(self, customer_id: str, text: str, source: str) -> SentimentInsight:
        """Create fallback text sentiment analysis"""
        # Simple keyword-based sentiment
        positive_words = ["good", "great", "excellent", "love", "amazing", "perfect", "satisfied"]
        negative_words = ["bad", "terrible", "awful", "hate", "problem", "issue", "disappointed"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment_score = 0.6
            urgency = "low"
        elif negative_count > positive_count:
            sentiment_score = -0.6
            urgency = "high"
        else:
            sentiment_score = 0.0
            urgency = "medium"
        
        return SentimentInsight(
            insight_id=str(uuid.uuid4()),
            customer_id=customer_id,
            source=source,
            text_sample=text[:200] + "..." if len(text) > 200 else text,
            sentiment_score=sentiment_score,
            emotions_detected=["positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"],
            topics_mentioned=["software", "service"],
            urgency_level=urgency,
            suggested_response="Thank you for your feedback. We value your input and will address any concerns."
        )
    
    async def _generate_sample_sentiment_dashboard(self) -> Dict[str, Any]:
        """Generate sample sentiment dashboard data"""
        return {
            "sentiment_overview": {
                "total_customers_analyzed": 50,
                "average_sentiment": 0.15,
                "positive_customers": 28,
                "neutral_customers": 18,
                "negative_customers": 4,
                "high_risk_count": 2,
                "advocate_count": 12
            },
            "sentiment_distribution": {
                "very_positive": 8,
                "positive": 20,
                "neutral": 18,
                "negative": 3,
                "very_negative": 1
            },
            "satisfaction_metrics": {
                "product_satisfaction": 0.72,
                "service_satisfaction": 0.68,
                "value_perception": 0.65,
                "recommendation_likelihood": 0.58
            },
            "top_sentiment_drivers": [
                {"driver": "Product quality", "count": 15},
                {"driver": "Customer support", "count": 12},
                {"driver": "Value for money", "count": 10}
            ],
            "risk_alerts": {
                "high_risk_customers": ["demo_2", "demo_4"],
                "trending_concerns": ["Support response time", "Feature requests"],
                "urgent_interventions": 2
            },
            "opportunities": {
                "positive_advocates": ["demo_1", "demo_3"],
                "improvement_areas": ["Service satisfaction", "Response time"],
                "engagement_boost_potential": 18
            }
        }
    
    async def _store_sentiment_results(self, profiles: List[SentimentProfile]):
        """Store sentiment analysis results"""
        try:
            document = {
                "analysis_id": str(uuid.uuid4()),
                "created_at": datetime.now(),
                "profiles": [profile.dict() for profile in profiles],
                "service": "sentiment_analysis"
            }
            
            await self.db.sentiment_analysis.insert_one(document)
            
        except Exception as e:
            print(f"Error storing sentiment results: {e}")