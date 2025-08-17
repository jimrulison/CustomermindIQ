"""
Customer Mind IQ - Base Connector
Universal connector interface for any business software integration
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod
from pydantic import BaseModel
import uuid

class UniversalCustomer(BaseModel):
    """Universal customer data model that works across all platforms"""
    customer_id: str
    platform_customer_id: str  # Original ID in the source platform
    platform_name: str  # stripe, odoo, shopify, etc.
    email: str
    name: Optional[str] = None
    created_date: Optional[datetime] = None
    total_spent: float = 0.0
    total_orders: int = 0
    last_order_date: Optional[datetime] = None
    status: str = "active"  # active, inactive, churned
    metadata: Dict[str, Any] = {}

class UniversalTransaction(BaseModel):
    """Universal transaction data model"""
    transaction_id: str
    platform_transaction_id: str
    platform_name: str
    customer_id: str
    amount: float
    currency: str = "USD"
    transaction_date: datetime
    transaction_type: str  # purchase, refund, subscription
    product_ids: List[str] = []
    status: str = "completed"
    metadata: Dict[str, Any] = {}

class UniversalProduct(BaseModel):
    """Universal product/service data model"""
    product_id: str
    platform_product_id: str
    platform_name: str
    name: str
    category: Optional[str] = None
    price: float = 0.0
    currency: str = "USD"
    description: Optional[str] = None
    metadata: Dict[str, Any] = {}

class ConnectorStatus(BaseModel):
    """Connector health and status information"""
    connector_name: str
    platform_name: str
    is_connected: bool
    last_sync: Optional[datetime] = None
    total_customers: int = 0
    total_transactions: int = 0
    error_message: Optional[str] = None
    sync_frequency: str = "hourly"  # hourly, daily, weekly

class BaseConnector(ABC):
    """
    Base connector class that all platform integrations must inherit from.
    Provides universal interface for customer intelligence data extraction.
    """
    
    def __init__(self, credentials: Dict[str, str]):
        self.credentials = credentials
        self.connector_id = str(uuid.uuid4())
        self.platform_name = self.get_platform_name()
        self.is_connected = False
        self.last_sync = None
        
    @abstractmethod
    def get_platform_name(self) -> str:
        """Return the name of the platform (e.g., 'stripe', 'odoo', 'shopify')"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Test if the connection to the platform is working"""
        pass
    
    @abstractmethod
    async def sync_customers(self, limit: int = 100) -> List[UniversalCustomer]:
        """
        Fetch customers from the platform and convert to universal format
        Args:
            limit: Maximum number of customers to fetch
        Returns:
            List of UniversalCustomer objects
        """
        pass
    
    @abstractmethod
    async def sync_transactions(self, days_back: int = 30, limit: int = 1000) -> List[UniversalTransaction]:
        """
        Fetch recent transactions from the platform
        Args:
            days_back: How many days back to fetch transactions
            limit: Maximum number of transactions to fetch
        Returns:
            List of UniversalTransaction objects
        """
        pass
    
    @abstractmethod
    async def sync_products(self, limit: int = 100) -> List[UniversalProduct]:
        """
        Fetch products/services from the platform
        Args:
            limit: Maximum number of products to fetch
        Returns:
            List of UniversalProduct objects
        """
        pass
    
    async def get_connector_status(self) -> ConnectorStatus:
        """Get current status and health of the connector"""
        try:
            is_connected = await self.test_connection()
            
            return ConnectorStatus(
                connector_name=f"{self.platform_name}_connector",
                platform_name=self.platform_name,
                is_connected=is_connected,
                last_sync=self.last_sync,
                total_customers=0,  # Will be updated during sync
                total_transactions=0,  # Will be updated during sync
                error_message=None if is_connected else "Connection failed",
                sync_frequency="hourly"
            )
        except Exception as e:
            return ConnectorStatus(
                connector_name=f"{self.platform_name}_connector",
                platform_name=self.platform_name,
                is_connected=False,
                last_sync=self.last_sync,
                total_customers=0,
                total_transactions=0,
                error_message=str(e),
                sync_frequency="hourly"
            )
    
    async def full_sync(self) -> Dict[str, Any]:
        """
        Perform a complete sync of all data from the platform
        Returns:
            Summary of synced data
        """
        try:
            # Test connection first
            if not await self.test_connection():
                raise Exception(f"Cannot connect to {self.platform_name}")
            
            # Sync all data types
            customers = await self.sync_customers()
            transactions = await self.sync_transactions()
            products = await self.sync_products()
            
            self.last_sync = datetime.now()
            self.is_connected = True
            
            return {
                "success": True,
                "platform": self.platform_name,
                "customers_synced": len(customers),
                "transactions_synced": len(transactions),
                "products_synced": len(products),
                "sync_time": self.last_sync,
                "customers": customers,
                "transactions": transactions,
                "products": products
            }
            
        except Exception as e:
            return {
                "success": False,
                "platform": self.platform_name,
                "error": str(e),
                "customers_synced": 0,
                "transactions_synced": 0,
                "products_synced": 0
            }
    
    def normalize_email(self, email: str) -> str:
        """Normalize email addresses for consistent customer matching"""
        if not email:
            return ""
        return email.lower().strip()
    
    def generate_universal_customer_id(self, platform_customer_id: str) -> str:
        """Generate universal customer ID that includes platform info"""
        return f"{self.platform_name}_{platform_customer_id}"
    
    def generate_universal_transaction_id(self, platform_transaction_id: str) -> str:
        """Generate universal transaction ID"""
        return f"{self.platform_name}_{platform_transaction_id}"
    
    def generate_universal_product_id(self, platform_product_id: str) -> str:
        """Generate universal product ID"""
        return f"{self.platform_name}_{platform_product_id}"