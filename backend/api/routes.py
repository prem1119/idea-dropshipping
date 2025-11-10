"""API routes for the dropshipping automation system."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime

from backend.models.schemas import (
    Product, StoreConfig, AdCampaign, Order, 
    CustomerMessage, DashboardMetrics
)
from backend.services.product_discovery import ProductDiscoveryService
from backend.services.shopify_manager import ShopifyManager
from backend.services.ad_manager import AdManager
from backend.services.order_fulfillment import OrderFulfillmentService
from backend.services.customer_service_agent import CustomerServiceAgent
from backend.services.analytics import AnalyticsService

router = APIRouter()


@router.get("/products/discover", response_model=List[Product])
async def discover_products(
    category: Optional[str] = None,
    min_margin: Optional[float] = None,
    limit: int = 20
):
    """Discover trending and high-margin products."""
    service = ProductDiscoveryService()
    products = await service.discover_products(
        category=category,
        min_margin=min_margin,
        limit=limit
    )
    return products


@router.post("/store/create")
async def create_store(config: StoreConfig):
    """Create or update Shopify store configuration."""
    manager = ShopifyManager()
    store = await manager.create_store(config)
    return {"status": "success", "store": store}


@router.post("/products/add")
async def add_product(product: Product):
    """Add product to Shopify store."""
    manager = ShopifyManager()
    result = await manager.add_product(product)
    return {"status": "success", "product": result}


@router.post("/ads/create", response_model=AdCampaign)
async def create_ad_campaign(campaign: AdCampaign):
    """Create ad campaign on TikTok/Facebook."""
    manager = AdManager()
    created = await manager.create_campaign(campaign)
    return created


@router.get("/ads/campaigns", response_model=List[AdCampaign])
async def list_campaigns():
    """List all ad campaigns."""
    manager = AdManager()
    campaigns = await manager.list_campaigns()
    return campaigns


@router.get("/orders/pending", response_model=List[Order])
async def get_pending_orders():
    """Get pending orders that need fulfillment."""
    service = OrderFulfillmentService()
    orders = await service.get_pending_orders()
    return orders


@router.post("/orders/{order_id}/fulfill")
async def fulfill_order(order_id: str):
    """Manually trigger order fulfillment."""
    service = OrderFulfillmentService()
    result = await service.fulfill_order(order_id)
    return {"status": "success", "fulfillment": result}


@router.get("/customer/messages", response_model=List[CustomerMessage])
async def get_customer_messages(answered: bool = False):
    """Get customer service messages."""
    agent = CustomerServiceAgent()
    messages = await agent.get_messages(answered=answered)
    return messages


@router.post("/customer/messages/{message_id}/respond")
async def respond_to_message(message_id: str):
    """Auto-respond to customer message."""
    agent = CustomerServiceAgent()
    response = await agent.handle_message(message_id)
    return {"status": "success", "response": response}


@router.get("/dashboard/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """Get dashboard metrics."""
    service = AnalyticsService()
    metrics = await service.get_metrics(start_date, end_date)
    return metrics


@router.post("/automation/start")
async def start_automation():
    """Start the full automation system."""
    # This will be handled by the orchestrator
    return {"status": "automation_started", "message": "Full automation system is now active"}


@router.post("/automation/stop")
async def stop_automation():
    """Stop the automation system."""
    return {"status": "automation_stopped"}

