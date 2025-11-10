"""Pydantic schemas for API models."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class ProductStatus(str, Enum):
    """Product status enum."""
    DISCOVERED = "discovered"
    LISTED = "listed"
    ACTIVE = "active"
    PAUSED = "paused"
    DELETED = "deleted"


class Product(BaseModel):
    """Product model."""
    id: Optional[str] = None
    title: str
    description: str
    price: float
    cost: float
    margin: float
    profit: float
    currency: str = "USD"
    category: str
    images: List[str] = []
    supplier_id: str
    supplier_name: str
    supplier_url: str
    shipping_info: Dict = {}
    status: ProductStatus = ProductStatus.DISCOVERED
    created_at: Optional[datetime] = None


class StoreConfig(BaseModel):
    """Shopify store configuration."""
    store_name: str
    store_url: str
    theme: str = "modern"
    brand_name: str
    brand_description: str
    logo_url: Optional[str] = None
    primary_color: str = "#000000"
    secondary_color: str = "#ffffff"
    payment_methods: List[str] = ["credit_card", "paypal"]
    shipping_zones: List[Dict] = []


class AdPlatform(str, Enum):
    """Ad platform enum."""
    TIKTOK = "tiktok"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"


class AdCampaign(BaseModel):
    """Ad campaign model."""
    id: Optional[str] = None
    name: str
    platform: AdPlatform
    product_id: str
    budget: float
    daily_budget: Optional[float] = None
    target_audience: Dict = {}
    creative_video_url: Optional[str] = None
    creative_caption: str
    status: str = "draft"
    created_at: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Order(BaseModel):
    """Order model."""
    id: str
    order_number: str
    customer_name: str
    customer_email: str
    items: List[Dict]
    total: float
    currency: str = "USD"
    shipping_address: Dict
    status: str = "pending"
    fulfillment_status: str = "unfulfilled"
    tracking_number: Optional[str] = None
    created_at: datetime


class CustomerMessage(BaseModel):
    """Customer message model."""
    id: str
    customer_name: str
    customer_email: str
    subject: str
    message: str
    order_id: Optional[str] = None
    answered: bool = False
    ai_response: Optional[str] = None
    created_at: datetime
    responded_at: Optional[datetime] = None


class DashboardMetrics(BaseModel):
    """Dashboard metrics model."""
    total_sales: float
    total_profit: float
    total_orders: int
    total_ad_spend: float
    roi: float
    conversion_rate: float
    average_order_value: float
    top_products: List[Dict]
    sales_by_date: List[Dict]
    profit_by_date: List[Dict]
    ad_performance: List[Dict]

