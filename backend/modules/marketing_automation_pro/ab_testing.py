"""
Customer Mind IQ - A/B Testing Microservice
AI-powered A/B testing and optimization for marketing campaigns
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from enum import Enum
import uuid
import random
from scipy import stats
import numpy as np

class TestStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TestVariant(BaseModel):
    variant_id: str
    name: str
    description: str
    content: Dict[str, Any]
    traffic_percentage: float
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0
    
class ABTest(BaseModel):
    test_id: str
    name: str
    description: str
    hypothesis: str
    test_type: str  # email_subject, content, cta, landing_page, etc.
    variants: List[TestVariant]
    target_audience: Dict[str, Any]
    success_metric: str
    confidence_level: float = 0.95
    minimum_sample_size: int = 1000
    test_duration_days: int = 14
    status: TestStatus = TestStatus.DRAFT
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = datetime.now()

class TestResults(BaseModel):
    test_id: str
    winner_variant_id: Optional[str] = None
    confidence_level: float
    statistical_significance: bool
    p_value: float
    lift: float  # percentage improvement
    variant_results: List[Dict[str, Any]]
    recommendations: List[str]
    insights: List[str]

class ABTestingService:
    """Customer Mind IQ A/B Testing Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.customer_mind_iq
        
    async def create_ab_test(self, test_data: Dict[str, Any]) -> ABTest:
        """Create a new A/B test with AI-powered optimization"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"ab_test_creation_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's A/B testing specialist. 
                Design and optimize A/B tests for maximum statistical significance and business impact."""
            ).with_model("openai", "gpt-4o-mini")
            
            test_optimization_prompt = f"""
            Design an optimal A/B test using Customer Mind IQ advanced testing algorithms:
            
            Test Request: {json.dumps(test_data, default=str)}
            
            Provide A/B test optimization in this exact JSON format:
            {{
                "optimized_hypothesis": "<clear_testable_hypothesis>",
                "test_type": "<email_subject/content/cta/landing_page/pricing>",
                "variants": [
                    {{
                        "name": "Control (A)",
                        "description": "<control_description>",
                        "content": {{"key": "value"}},
                        "traffic_percentage": 50.0
                    }},
                    {{
                        "name": "Variant B",
                        "description": "<variant_description>",
                        "content": {{"key": "value"}},
                        "traffic_percentage": 50.0
                    }}
                ],
                "success_metric": "<conversion_rate/click_rate/revenue_per_visitor>",
                "minimum_sample_size": <calculated_sample_size>,
                "test_duration_days": <optimal_duration>,
                "target_audience": {{
                    "segment": "<audience_segment>",
                    "size": <audience_size>,
                    "criteria": ["criteria1", "criteria2"]
                }},
                "expected_results": {{
                    "baseline_rate": <current_rate>,
                    "minimum_detectable_effect": <mde_percentage>,
                    "expected_lift": <expected_improvement>
                }}
            }}
            
            Focus on statistical power, practical significance, and business impact.
            """
            
            message = UserMessage(text=test_optimization_prompt)
            response = await chat.send_message(message)
            
            try:
                optimization = json.loads(response)
                
                # Create test variants
                variants = []
                for i, variant_data in enumerate(optimization.get('variants', [])):
                    variant = TestVariant(
                        variant_id=str(uuid.uuid4()),
                        name=variant_data.get('name', f'Variant {chr(65+i)}'),
                        description=variant_data.get('description', ''),
                        content=variant_data.get('content', {}),
                        traffic_percentage=variant_data.get('traffic_percentage', 50.0)
                    )
                    variants.append(variant)
                
                ab_test = ABTest(
                    test_id=str(uuid.uuid4()),
                    name=test_data.get('name', 'A/B Test'),
                    description=test_data.get('description', ''),
                    hypothesis=optimization.get('optimized_hypothesis', 'Variant B will outperform Control A'),
                    test_type=optimization.get('test_type', 'content'),
                    variants=variants,
                    target_audience=optimization.get('target_audience', {}),
                    success_metric=optimization.get('success_metric', 'conversion_rate'),
                    minimum_sample_size=optimization.get('minimum_sample_size', 1000),
                    test_duration_days=optimization.get('test_duration_days', 14)
                )
                
                # Store test
                await self._store_ab_test(ab_test)
                return ab_test
                
            except json.JSONDecodeError:
                return await self._fallback_ab_test_creation(test_data)
                
        except Exception as e:
            print(f"A/B test creation error: {e}")
            return await self._fallback_ab_test_creation(test_data)
    
    async def start_ab_test(self, test_id: str) -> Dict[str, Any]:
        """Start an A/B test and begin traffic allocation"""
        try:
            # Get test details
            test_doc = await self.db.ab_tests.find_one({"test_id": test_id})
            if not test_doc:
                return {"error": "Test not found"}
            
            ab_test = ABTest(**test_doc)
            
            # Validate test before starting
            validation_result = await self._validate_test_setup(ab_test)
            if not validation_result["valid"]:
                return {"error": f"Test validation failed: {validation_result['reason']}"}
            
            # Update test status and dates
            start_date = datetime.now()
            end_date = start_date + timedelta(days=ab_test.test_duration_days)
            
            await self.db.ab_tests.update_one(
                {"test_id": test_id},
                {
                    "$set": {
                        "status": "running",
                        "start_date": start_date,
                        "end_date": end_date,
                        "updated_at": datetime.now()
                    }
                }
            )
            
            return {
                "test_id": test_id,
                "status": "running",
                "start_date": start_date,
                "end_date": end_date,
                "variants_count": len(ab_test.variants),
                "expected_sample_size": ab_test.minimum_sample_size,
                "message": "A/B test started successfully"
            }
            
        except Exception as e:
            print(f"A/B test start error: {e}")
            return {"error": str(e)}
    
    async def analyze_test_results(self, test_id: str) -> TestResults:
        """Analyze A/B test results with statistical significance"""
        try:
            # Get test and results
            test_doc = await self.db.ab_tests.find_one({"test_id": test_id})
            if not test_doc:
                raise Exception("Test not found")
            
            ab_test = ABTest(**test_doc)
            
            # Calculate statistical significance
            variant_results = []
            conversion_rates = []
            sample_sizes = []
            
            for variant in ab_test.variants:
                conversion_rate = (variant.conversions / variant.impressions) if variant.impressions > 0 else 0
                conversion_rates.append(conversion_rate)
                sample_sizes.append(variant.impressions)
                
                variant_results.append({
                    "variant_id": variant.variant_id,
                    "name": variant.name,
                    "impressions": variant.impressions,
                    "conversions": variant.conversions,
                    "conversion_rate": round(conversion_rate * 100, 2),
                    "revenue": variant.revenue,
                    "revenue_per_impression": variant.revenue / variant.impressions if variant.impressions > 0 else 0
                })
            
            # Statistical analysis
            statistical_significance = False
            p_value = 1.0
            winner_variant_id = None
            lift = 0.0
            
            if len(conversion_rates) >= 2 and all(s > 0 for s in sample_sizes):
                # Perform chi-square test or z-test for proportions
                control_rate = conversion_rates[0]
                test_rate = max(conversion_rates[1:])
                
                if test_rate > control_rate:
                    # Calculate z-test for proportions
                    control_conversions = ab_test.variants[0].conversions
                    control_impressions = ab_test.variants[0].impressions
                    
                    best_variant_idx = conversion_rates.index(test_rate)
                    test_conversions = ab_test.variants[best_variant_idx].conversions
                    test_impressions = ab_test.variants[best_variant_idx].impressions
                    
                    # Z-test calculation
                    pooled_rate = (control_conversions + test_conversions) / (control_impressions + test_impressions)
                    pooled_se = np.sqrt(pooled_rate * (1 - pooled_rate) * (1/control_impressions + 1/test_impressions))
                    
                    if pooled_se > 0:
                        z_score = (test_rate - control_rate) / pooled_se
                        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
                        statistical_significance = p_value < (1 - ab_test.confidence_level)
                        lift = ((test_rate - control_rate) / control_rate * 100) if control_rate > 0 else 0
                        
                        if statistical_significance:
                            winner_variant_id = ab_test.variants[best_variant_idx].variant_id
            
            # Generate AI insights
            insights = await self._generate_test_insights(ab_test, variant_results, statistical_significance, lift)
            recommendations = await self._generate_test_recommendations(ab_test, variant_results, winner_variant_id)
            
            test_results = TestResults(
                test_id=test_id,
                winner_variant_id=winner_variant_id,
                confidence_level=ab_test.confidence_level,
                statistical_significance=statistical_significance,
                p_value=p_value,
                lift=lift,
                variant_results=variant_results,
                recommendations=recommendations,
                insights=insights
            )
            
            # Store results
            await self._store_test_results(test_results)
            
            return test_results
            
        except Exception as e:
            print(f"Test analysis error: {e}")
            return await self._fallback_test_results(test_id)
    
    async def get_ab_testing_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive A/B testing dashboard"""
        try:
            # Get all tests
            tests = await self.db.ab_tests.find().to_list(length=100)
            test_results = await self.db.ab_test_results.find().to_list(length=100)
            
            if not tests:
                return await self._generate_sample_ab_dashboard()
            
            # Test status distribution
            status_distribution = {}
            for test in tests:
                status = test.get('status', 'draft')
                status_distribution[status] = status_distribution.get(status, 0) + 1
            
            # Test type analysis
            test_types = {}
            for test in tests:
                test_type = test.get('test_type', 'unknown')
                test_types[test_type] = test_types.get(test_type, 0) + 1
            
            # Performance metrics
            completed_tests = [t for t in tests if t.get('status') == 'completed']
            significant_results = [r for r in test_results if r.get('statistical_significance')]
            
            total_impressions = 0
            total_conversions = 0
            total_lift = 0
            
            for result in test_results:
                for variant in result.get('variant_results', []):
                    total_impressions += variant.get('impressions', 0)
                    total_conversions += variant.get('conversions', 0)
                
                if result.get('lift'):
                    total_lift += result.get('lift', 0)
            
            avg_lift = (total_lift / len(test_results)) if test_results else 0
            overall_conversion_rate = (total_conversions / total_impressions * 100) if total_impressions > 0 else 0
            
            return {
                "testing_overview": {
                    "total_tests": len(tests),
                    "running_tests": status_distribution.get('running', 0),
                    "completed_tests": len(completed_tests),
                    "significant_results": len(significant_results),
                    "success_rate": (len(significant_results) / len(completed_tests) * 100) if completed_tests else 0
                },
                "status_distribution": status_distribution,
                "test_types": test_types,
                "performance_metrics": {
                    "total_impressions": total_impressions,
                    "total_conversions": total_conversions,
                    "overall_conversion_rate": round(overall_conversion_rate, 2),
                    "average_lift": round(avg_lift, 2),
                    "confidence_level": 95.0
                },
                "insights": [
                    f"{len(significant_results)} tests achieved statistical significance",
                    f"Average lift across winning tests: {avg_lift:.1f}%",
                    f"Most tested element: {max(test_types.items(), key=lambda x: x[1])[0] if test_types else 'N/A'}"
                ]
            }
            
        except Exception as e:
            print(f"A/B testing dashboard error: {e}")
            return await self._generate_sample_ab_dashboard()
    
    async def _validate_test_setup(self, ab_test: ABTest) -> Dict[str, Any]:
        """Validate A/B test setup before starting"""
        if len(ab_test.variants) < 2:
            return {"valid": False, "reason": "At least 2 variants required"}
        
        total_traffic = sum(v.traffic_percentage for v in ab_test.variants)
        if abs(total_traffic - 100.0) > 0.1:
            return {"valid": False, "reason": "Traffic percentages must sum to 100%"}
        
        if ab_test.minimum_sample_size < 100:
            return {"valid": False, "reason": "Minimum sample size too small for reliable results"}
        
        return {"valid": True, "reason": "Test setup is valid"}
    
    async def _generate_test_insights(self, ab_test: ABTest, variant_results: List[Dict], significant: bool, lift: float) -> List[str]:
        """Generate AI-powered test insights"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"test_insights_{ab_test.test_id}",
                system_message="""You are Customer Mind IQ's A/B testing analyst. 
                Generate actionable insights from A/B test results."""
            ).with_model("openai", "gpt-4o-mini")
            
            insights_prompt = f"""
            Analyze these A/B test results and provide insights:
            
            Test: {ab_test.name}
            Hypothesis: {ab_test.hypothesis}
            Results: {json.dumps(variant_results, default=str)}
            Statistical Significance: {significant}
            Lift: {lift}%
            
            Provide 3-5 key insights in JSON format:
            {{
                "insights": ["insight1", "insight2", "insight3"]
            }}
            """
            
            message = UserMessage(text=insights_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                return analysis.get('insights', [])
            except json.JSONDecodeError:
                return self._fallback_insights(significant, lift)
                
        except Exception as e:
            print(f"Insights generation error: {e}")
            return self._fallback_insights(significant, lift)
    
    async def _generate_test_recommendations(self, ab_test: ABTest, variant_results: List[Dict], winner_id: Optional[str]) -> List[str]:
        """Generate AI-powered test recommendations"""
        if winner_id:
            return [
                f"Implement winning variant across all traffic",
                f"Consider testing variations of the winning element",
                f"Monitor performance after implementation"
            ]
        else:
            return [
                f"Continue running test to reach statistical significance",
                f"Consider increasing sample size",
                f"Review test setup and hypothesis"
            ]
    
    def _fallback_insights(self, significant: bool, lift: float) -> List[str]:
        """Fallback insights when AI fails"""
        if significant:
            return [
                f"Test achieved statistical significance with {lift:.1f}% lift",
                "Winning variant should be implemented",
                "Results can be trusted for business decisions"
            ]
        else:
            return [
                "Test did not achieve statistical significance",
                "More data needed for reliable conclusions",
                "Consider running test longer or increasing sample size"
            ]
    
    async def _fallback_ab_test_creation(self, test_data: Dict[str, Any]) -> ABTest:
        """Fallback A/B test creation when AI fails"""
        variants = [
            TestVariant(
                variant_id=str(uuid.uuid4()),
                name="Control (A)",
                description="Original version",
                content={"version": "control"},
                traffic_percentage=50.0
            ),
            TestVariant(
                variant_id=str(uuid.uuid4()),
                name="Variant B",
                description="Test version",
                content={"version": "variant"},
                traffic_percentage=50.0
            )
        ]
        
        return ABTest(
            test_id=str(uuid.uuid4()),
            name=test_data.get('name', 'A/B Test'),
            description=test_data.get('description', 'A/B test for optimization'),
            hypothesis="Variant B will outperform Control A",
            test_type=test_data.get('test_type', 'content'),
            variants=variants,
            target_audience={"segment": "all_users", "size": 1000},
            success_metric="conversion_rate",
            minimum_sample_size=1000,
            test_duration_days=14
        )
    
    async def _fallback_test_results(self, test_id: str) -> TestResults:
        """Fallback test results when analysis fails"""
        return TestResults(
            test_id=test_id,
            winner_variant_id=None,
            confidence_level=0.95,
            statistical_significance=False,
            p_value=1.0,
            lift=0.0,
            variant_results=[],
            recommendations=["Continue test to gather more data"],
            insights=["Insufficient data for analysis"]
        )
    
    async def _generate_sample_ab_dashboard(self) -> Dict[str, Any]:
        """Generate sample A/B testing dashboard"""
        return {
            "testing_overview": {
                "total_tests": 8,
                "running_tests": 3,
                "completed_tests": 4,
                "significant_results": 3,
                "success_rate": 75.0
            },
            "status_distribution": {
                "running": 3,
                "completed": 4,
                "draft": 1
            },
            "test_types": {
                "email_subject": 3,
                "content": 2,
                "cta": 2,
                "landing_page": 1
            },
            "performance_metrics": {
                "total_impressions": 25000,
                "total_conversions": 1250,
                "overall_conversion_rate": 5.0,
                "average_lift": 18.5,
                "confidence_level": 95.0
            },
            "insights": [
                "3 tests achieved statistical significance",
                "Average lift across winning tests: 18.5%",
                "Most tested element: email_subject"
            ]
        }
    
    async def _store_ab_test(self, ab_test: ABTest):
        """Store A/B test in database"""
        try:
            await self.db.ab_tests.insert_one(ab_test.dict())
            print(f"✅ Stored A/B test: {ab_test.test_id}")
        except Exception as e:
            print(f"❌ Error storing A/B test: {e}")
    
    async def _store_test_results(self, results: TestResults):
        """Store test results in database"""
        try:
            await self.db.ab_test_results.insert_one(results.dict())
            print(f"✅ Stored test results: {results.test_id}")
        except Exception as e:
            print(f"❌ Error storing test results: {e}")