"""
Customer Mind IQ - Universal Business Connectors
Multi-platform integration system for customer intelligence
"""

from .base_connector import BaseConnector
from .stripe_connector import StripeConnector
from .odoo_connector import OdooConnector

__all__ = [
    'BaseConnector',
    'StripeConnector', 
    'OdooConnector'
]