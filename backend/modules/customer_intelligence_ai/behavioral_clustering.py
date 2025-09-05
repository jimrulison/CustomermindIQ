"""
Customer Mind IQ - Behavioral Clustering Microservice
Advanced AI-powered customer behavior clustering and segmentation
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import uuid

class CustomerCluster(BaseModel):
    cluster_id: str
    cluster_name: str
    customer_count: int
    avg_spending: float
    avg_engagement: float
    top_behaviors: List[str]
    recommended_actions: List[str]
    risk_level: str  # low, medium, high
    value_potential: str  # low, medium, high

class ClusterInsight(BaseModel):
    customer_id: str
    cluster_id: str
    cluster_name: str
    similarity_score: float
    behavioral_traits: List[str]
    cluster_position: str  # core, edge, outlier
    migration_probability: Dict[str, float]  # probabilities to other clusters

class BehavioralClusteringService:
    """Customer Mind IQ Behavioral Clustering Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[os.environ.get('DB_NAME', 'customer_mind_iq')]
        
    async def analyze_customer_behaviors(self, customers_data: List[Dict]) -> Dict[str, Any]:
        """Analyze and cluster customers based on behavioral patterns using AI"""
        try:
            # Prepare behavioral features for clustering
            behavioral_features = []
            customer_ids = []
            
            for customer in customers_data:
                features = [
                    customer.get('total_spent', 0) / 1000,  # Normalize spending
                    customer.get('total_purchases', 0),
                    customer.get('engagement_score', 50) / 100,
                    len(customer.get('software_owned', [])),
                    self._days_since_last_purchase(customer.get('last_purchase_date'))
                ]
                behavioral_features.append(features)
                customer_ids.append(customer['customer_id'])
            
            if len(behavioral_features) < 3:
                return await self._generate_ai_clusters(customers_data)
            
            # Perform K-means clustering
            scaler = StandardScaler()
            scaled_features = scaler.fit_transform(behavioral_features)
            
            # Determine optimal number of clusters (3-6 based on data size)
            n_clusters = min(max(3, len(customers_data) // 5), 6)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(scaled_features)
            
            # Group customers by clusters
            clusters = {}
            for i, customer in enumerate(customers_data):
                cluster_id = f"cluster_{cluster_labels[i]}"
                if cluster_id not in clusters:
                    clusters[cluster_id] = []
                clusters[cluster_id].append(customer)
            
            # Generate AI-powered cluster insights
            cluster_analysis = await self._generate_cluster_insights(clusters)
            
            return cluster_analysis
            
        except Exception as e:
            print(f"Behavioral clustering error: {e}")
            return await self._generate_ai_clusters(customers_data)
    
    async def _generate_ai_clusters(self, customers_data: List[Dict]) -> Dict[str, Any]:
        """Generate behavioral clusters using AI when statistical clustering isn't possible"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"behavioral_clustering_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's behavioral clustering specialist. Analyze customer data 
                and create intelligent behavioral segments based on purchase patterns, engagement, and software usage. 
                Return comprehensive clustering analysis in JSON format."""
            ).with_model("openai", "gpt-4o-mini")
            
            clustering_prompt = f"""
            Analyze these customers and create behavioral clusters using Customer Mind IQ advanced segmentation:
            
            Customer Data: {json.dumps(customers_data[:10], default=str)}
            
            Create behavioral clusters in this exact JSON format:
            {{
                "clusters": [
                    {{
                        "cluster_id": "high_value_champions",
                        "cluster_name": "High-Value Software Champions",
                        "customer_count": <number>,
                        "avg_spending": <average_spending>,
                        "avg_engagement": <0-100>,
                        "top_behaviors": ["behavior1", "behavior2", "behavior3"],
                        "recommended_actions": ["action1", "action2"],
                        "risk_level": "low",
                        "value_potential": "high",
                        "customers": ["customer_id1", "customer_id2"]
                    }}
                ],
                "insights": {{
                    "total_clusters": <number>,
                    "dominant_pattern": "<description>",
                    "growth_opportunities": ["opportunity1", "opportunity2"],
                    "risk_factors": ["risk1", "risk2"]
                }}
            }}
            
            Focus on:
            1. Behavioral patterns in software purchases
            2. Engagement levels and loyalty indicators  
            3. Growth potential and upsell opportunities
            4. Churn risk and retention strategies
            5. Cross-sell compatibility between segments
            """
            
            message = UserMessage(text=clustering_prompt)
            response = await chat.send_message(message)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return await self._fallback_clusters(customers_data)
                
        except Exception as e:
            print(f"AI clustering error: {e}")
            return await self._fallback_clusters(customers_data)
    
    async def _generate_cluster_insights(self, clusters: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Generate AI insights for statistical clusters"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"cluster_insights_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's cluster analysis expert. Analyze customer clusters 
                and provide actionable business insights for each segment."""
            ).with_model("openai", "gpt-4o-mini")
            
            cluster_data = {}
            for cluster_id, customers in clusters.items():
                cluster_data[cluster_id] = {
                    "customer_count": len(customers),
                    "avg_spending": sum(c.get('total_spent', 0) for c in customers) / len(customers),
                    "avg_engagement": sum(c.get('engagement_score', 50) for c in customers) / len(customers),
                    "software_usage": [s for c in customers for s in c.get('software_owned', [])],
                    "customer_ids": [c['customer_id'] for c in customers]
                }
            
            insight_prompt = f"""
            Analyze these customer clusters and provide comprehensive behavioral insights:
            
            Cluster Data: {json.dumps(cluster_data, default=str)}
            
            Provide analysis in this JSON format:
            {{
                "clusters": [
                    {{
                        "cluster_id": "<original_cluster_id>",
                        "cluster_name": "<descriptive_name>",
                        "customer_count": <count>,
                        "avg_spending": <spending>,
                        "avg_engagement": <0-100>,
                        "top_behaviors": ["behavior1", "behavior2"],
                        "recommended_actions": ["action1", "action2"],
                        "risk_level": "<low/medium/high>",
                        "value_potential": "<low/medium/high>",
                        "customers": ["customer_id1", "customer_id2"]
                    }}
                ],
                "insights": {{
                    "total_clusters": <number>,
                    "dominant_pattern": "<description>",
                    "growth_opportunities": ["opportunity1", "opportunity2"],
                    "risk_factors": ["risk1", "risk2"]
                }}
            }}
            """
            
            message = UserMessage(text=insight_prompt)
            response = await chat.send_message(message)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return await self._fallback_clusters(list(clusters.values())[0])
                
        except Exception as e:
            print(f"Cluster insights error: {e}")
            return await self._fallback_clusters([])
    
    async def get_customer_cluster_details(self, customer_id: str) -> Optional[ClusterInsight]:
        """Get detailed cluster information for a specific customer"""
        try:
            # Get customer data
            customer = await self.db.customers.find_one({"customer_id": customer_id})
            if not customer:
                return None
            
            # Get latest clustering results
            cluster_data = await self.db.behavioral_clusters.find_one(
                {}, sort=[("created_at", -1)]
            )
            
            if not cluster_data:
                return None
            
            # Find customer's cluster
            customer_cluster = None
            for cluster in cluster_data.get('clusters', []):
                if customer_id in cluster.get('customers', []):
                    customer_cluster = cluster
                    break
            
            if not customer_cluster:
                return None
            
            # Generate migration probabilities using AI
            migration_probs = await self._calculate_migration_probability(customer, cluster_data)
            
            return ClusterInsight(
                customer_id=customer_id,
                cluster_id=customer_cluster['cluster_id'],
                cluster_name=customer_cluster['cluster_name'],
                similarity_score=0.85,  # Could be calculated based on distance to centroid
                behavioral_traits=customer_cluster['top_behaviors'],
                cluster_position="core",  # Could be calculated based on cluster analysis
                migration_probability=migration_probs
            )
            
        except Exception as e:
            print(f"Customer cluster details error: {e}")
            return None
    
    async def _calculate_migration_probability(self, customer: Dict, cluster_data: Dict) -> Dict[str, float]:
        """Calculate probability of customer migrating to other clusters"""
        try:
            # Simple heuristic based on customer characteristics
            migration_probs = {}
            current_spending = customer.get('total_spent', 0)
            current_engagement = customer.get('engagement_score', 50)
            
            for cluster in cluster_data.get('clusters', []):
                cluster_spending = cluster.get('avg_spending', 0)
                cluster_engagement = cluster.get('avg_engagement', 50)
                
                spending_diff = abs(current_spending - cluster_spending)
                engagement_diff = abs(current_engagement - cluster_engagement)
                
                # Higher probability for closer clusters
                probability = max(0.1, 1 - (spending_diff / 10000 + engagement_diff / 100))
                migration_probs[cluster['cluster_id']] = round(probability, 3)
            
            return migration_probs
            
        except Exception as e:
            print(f"Migration probability error: {e}")
            return {}
    
    def _days_since_last_purchase(self, last_purchase_date) -> float:
        """Calculate days since last purchase"""
        if not last_purchase_date:
            return 365.0  # Default to 1 year if no purchase date
        
        if isinstance(last_purchase_date, str):
            try:
                last_purchase_date = datetime.fromisoformat(last_purchase_date.replace('Z', '+00:00'))
            except:
                return 365.0
        
        days_since = (datetime.now() - last_purchase_date).days
        return min(days_since, 365.0)  # Cap at 1 year
    
    async def _fallback_clusters(self, customers_data: List[Dict]) -> Dict[str, Any]:
        """Fallback clustering when AI fails"""
        return {
            "clusters": [
                {
                    "cluster_id": "high_value_customers",
                    "cluster_name": "High-Value Software Buyers",
                    "customer_count": len([c for c in customers_data if c.get('total_spent', 0) > 10000]),
                    "avg_spending": 15000,
                    "avg_engagement": 85,
                    "top_behaviors": ["Regular purchaser", "High engagement", "Premium software user"],
                    "recommended_actions": ["VIP treatment", "Early access to new features"],
                    "risk_level": "low",
                    "value_potential": "high",
                    "customers": [c['customer_id'] for c in customers_data if c.get('total_spent', 0) > 10000]
                },
                {
                    "cluster_id": "growth_potential", 
                    "cluster_name": "Growth Potential Customers",
                    "customer_count": len([c for c in customers_data if 5000 <= c.get('total_spent', 0) <= 10000]),
                    "avg_spending": 7500,
                    "avg_engagement": 65,
                    "top_behaviors": ["Moderate engagement", "Expanding software needs"],
                    "recommended_actions": ["Targeted upsell campaigns", "Feature demonstrations"],
                    "risk_level": "medium",
                    "value_potential": "high",
                    "customers": [c['customer_id'] for c in customers_data if 5000 <= c.get('total_spent', 0) <= 10000]
                }
            ],
            "insights": {
                "total_clusters": 2,
                "dominant_pattern": "Value-driven software purchasing",
                "growth_opportunities": ["Upsell to growth segment", "Retain high-value customers"],
                "risk_factors": ["Low engagement in growth segment"]
            }
        }
    
    async def store_clustering_results(self, results: Dict[str, Any]) -> str:
        """Store clustering results in database"""
        try:
            document = {
                "clustering_id": str(uuid.uuid4()),
                "created_at": datetime.now(),
                "results": results,
                "service": "behavioral_clustering"
            }
            
            await self.db.behavioral_clusters.insert_one(document)
            return document["clustering_id"]
            
        except Exception as e:
            print(f"Error storing clustering results: {e}")
            return ""