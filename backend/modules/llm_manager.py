"""
Customer Mind IQ - Advanced LLM Manager
Intelligent model selection and management system with latest AI models
"""

import os
import random
from typing import Dict, List, Optional, Tuple
from emergentintegrations.llm.chat import LlmChat, UserMessage
from enum import Enum

class ModelType(Enum):
    """Model types for different use cases"""
    FAST = "fast"  # Quick operations, analysis
    ADVANCED = "advanced"  # Complex reasoning, detailed analysis
    CREATIVE = "creative"  # Content generation, creative writing
    PREMIUM = "premium"  # Most advanced capabilities

class LLMProvider(Enum):
    """Available LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic" 
    GEMINI = "gemini"

class LLMManager:
    """
    Advanced LLM Manager with intelligent model selection
    Supports Claude Sonnet 4, GPT-5, Gemini 2.5 Pro
    """
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        
        # Latest model configurations (September 2025)
        self.models = {
            # Fast models for quick operations
            ModelType.FAST: [
                (LLMProvider.OPENAI, "gpt-5-mini"),
                (LLMProvider.ANTHROPIC, "claude-3-5-haiku-20241022"),
                (LLMProvider.GEMINI, "gemini-2.0-flash-lite"),
            ],
            
            # Advanced models for complex reasoning  
            ModelType.ADVANCED: [
                (LLMProvider.ANTHROPIC, "claude-4-sonnet-20250514"),  # Claude Sonnet 4 - Latest
                (LLMProvider.OPENAI, "gpt-5"),  # GPT-5 - Latest
                (LLMProvider.GEMINI, "gemini-2.5-pro"),  # Gemini 2.5 Pro - Latest
            ],
            
            # Creative models for content generation
            ModelType.CREATIVE: [
                (LLMProvider.OPENAI, "gpt-5"),
                (LLMProvider.ANTHROPIC, "claude-4-sonnet-20250514"),
                (LLMProvider.GEMINI, "gemini-2.5-flash"),
            ],
            
            # Premium models for most advanced capabilities
            ModelType.PREMIUM: [
                (LLMProvider.ANTHROPIC, "claude-4-opus-20250514"),  # Most advanced Claude
                (LLMProvider.OPENAI, "o3-pro"),  # Most advanced OpenAI
                (LLMProvider.GEMINI, "gemini-2.5-pro"),  # Most advanced Gemini
            ]
        }
        
        # Default provider preferences (user requested priority)
        self.provider_priority = [
            LLMProvider.ANTHROPIC,  # Claude (highest priority)
            LLMProvider.OPENAI,     # ChatGPT-5
            LLMProvider.GEMINI,     # Gemini 2.5 Pro
        ]
        
    def get_optimal_model(self, model_type: ModelType = ModelType.ADVANCED, 
                         preferred_provider: Optional[LLMProvider] = None) -> Tuple[str, str]:
        """
        Get optimal model for the given type and provider preference
        Returns (provider, model_name)
        """
        available_models = self.models[model_type]
        
        # If preferred provider specified, try that first
        if preferred_provider:
            for provider, model in available_models:
                if provider == preferred_provider:
                    return provider.value, model
        
        # Use priority order
        for priority_provider in self.provider_priority:
            for provider, model in available_models:
                if provider == priority_provider:
                    return provider.value, model
                    
        # Fallback to first available
        provider, model = available_models[0]
        return provider.value, model
    
    def create_chat(self, 
                   session_id: str,
                   system_message: str,
                   model_type: ModelType = ModelType.ADVANCED,
                   preferred_provider: Optional[LLMProvider] = None) -> LlmChat:
        """
        Create an optimized LLM chat instance
        """
        provider, model = self.get_optimal_model(model_type, preferred_provider)
        
        return LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        ).with_model(provider, model)
    
    def create_intelligence_chat(self, session_id: str, context: str = "customer intelligence") -> LlmChat:
        """Create chat optimized for customer intelligence analysis"""
        system_message = f"""You are Customer Mind IQ's advanced AI intelligence analyst. 
        Analyze {context} data to provide actionable insights and strategic recommendations.
        Focus on practical, measurable outcomes and business value."""
        
        return self.create_chat(
            session_id=session_id,
            system_message=system_message,
            model_type=ModelType.ADVANCED,
            preferred_provider=LLMProvider.ANTHROPIC  # Claude Sonnet 4 for intelligence
        )
    
    def create_growth_chat(self, session_id: str) -> LlmChat:
        """Create chat optimized for growth acceleration analysis"""
        system_message = """You are Customer Mind IQ's Growth Acceleration AI specialist.
        Analyze business data to identify high-impact growth opportunities, revenue optimization strategies,
        and actionable recommendations that drive measurable business growth."""
        
        return self.create_chat(
            session_id=session_id,
            system_message=system_message,
            model_type=ModelType.PREMIUM,
            preferred_provider=LLMProvider.OPENAI  # GPT-5 for advanced growth analysis
        )
    
    def create_creative_chat(self, session_id: str, context: str = "marketing") -> LlmChat:
        """Create chat optimized for creative content generation"""
        system_message = f"""You are Customer Mind IQ's creative AI specialist for {context}.
        Generate engaging, conversion-focused content that resonates with target audiences
        and drives business results. Focus on creativity, persuasion, and brand consistency."""
        
        return self.create_chat(
            session_id=session_id,
            system_message=system_message,
            model_type=ModelType.CREATIVE,
            preferred_provider=LLMProvider.GEMINI  # Gemini for creative tasks
        )
    
    def get_model_info(self) -> Dict:
        """Get information about available models"""
        return {
            "total_models": sum(len(models) for models in self.models.values()),
            "providers": [provider.value for provider in LLMProvider],
            "model_types": [model_type.value for model_type in ModelType],
            "latest_models": {
                "claude_sonnet_4": "claude-4-sonnet-20250514",
                "gpt_5": "gpt-5", 
                "gemini_2_5_pro": "gemini-2.5-pro",
                "most_advanced": "claude-4-opus-20250514"
            },
            "provider_priority": [p.value for p in self.provider_priority]
        }

# Global instance for easy access
llm_manager = LLMManager()