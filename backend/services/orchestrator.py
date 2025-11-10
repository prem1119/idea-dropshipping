"""Main automation orchestrator that coordinates all services."""
import asyncio
import logging
from typing import Optional
from datetime import datetime, timedelta

from backend.services.product_discovery import ProductDiscoveryService
from backend.services.shopify_manager import ShopifyManager
from backend.services.ad_manager import AdManager
from backend.services.order_fulfillment import OrderFulfillmentService
from backend.services.customer_service_agent import CustomerServiceAgent
from backend.services.analytics import AnalyticsService
from backend.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AutomationOrchestrator:
    """
    Main orchestrator that coordinates all automation workflows.
    Runs continuous automation loops for hands-free operation.
    """
    
    def __init__(self):
        self.product_discovery = ProductDiscoveryService()
        self.shopify_manager = ShopifyManager()
        self.ad_manager = AdManager()
        self.order_fulfillment = OrderFulfillmentService()
        self.customer_service = CustomerServiceAgent()
        self.analytics = AnalyticsService()
        
        self.running = False
        self.tasks = []
        
    async def initialize(self):
        """Initialize the orchestrator."""
        logger.info("Initializing automation orchestrator...")
        self.running = True
        
        # Start automation loops
        self.tasks = [
            asyncio.create_task(self._product_discovery_loop()),
            asyncio.create_task(self._order_fulfillment_loop()),
            asyncio.create_task(self._customer_service_loop()),
            asyncio.create_task(self._ad_optimization_loop())
        ]
        
        logger.info("Automation orchestrator initialized and running")
    
    async def shutdown(self):
        """Shutdown the orchestrator."""
        logger.info("Shutting down automation orchestrator...")
        self.running = False
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)
        
        logger.info("Automation orchestrator shut down")
    
    async def _product_discovery_loop(self):
        """Continuous loop for discovering and adding products."""
        logger.info("Starting product discovery loop")
        
        while self.running:
            try:
                await asyncio.sleep(3600)  # Run every hour
                
                if not settings.auto_ad_creation_enabled:
                    continue
                
                logger.info("Running product discovery...")
                
                # Discover trending products
                products = await self.product_discovery.discover_products(
                    min_margin=settings.min_profit_margin,
                    limit=5
                )
                
                # Add top products to store
                for product in products[:3]:  # Add top 3
                    try:
                        await self.shopify_manager.add_product(product)
                        logger.info(f"Added product: {product.title}")
                        
                        # Auto-create ad campaign for new products
                        if settings.auto_ad_creation_enabled:
                            await self._create_product_ad(product)
                            
                    except Exception as e:
                        logger.error(f"Error adding product {product.id}: {e}")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in product discovery loop: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _order_fulfillment_loop(self):
        """Continuous loop for automatic order fulfillment."""
        logger.info("Starting order fulfillment loop")
        
        while self.running:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                
                if not settings.auto_fulfill_enabled:
                    continue
                
                logger.info("Checking for pending orders...")
                
                # Get pending orders
                pending_orders = await self.order_fulfillment.get_pending_orders()
                
                # Fulfill each order
                for order in pending_orders:
                    try:
                        result = await self.order_fulfillment.fulfill_order(order.id)
                        if result.get("status") == "success":
                            logger.info(f"Fulfilled order: {order.order_number}")
                        else:
                            logger.warning(f"Failed to fulfill order {order.order_number}: {result.get('message')}")
                    except Exception as e:
                        logger.error(f"Error fulfilling order {order.id}: {e}")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in order fulfillment loop: {e}")
                await asyncio.sleep(300)
    
    async def _customer_service_loop(self):
        """Continuous loop for handling customer messages."""
        logger.info("Starting customer service loop")
        
        while self.running:
            try:
                await asyncio.sleep(180)  # Check every 3 minutes
                
                if not settings.auto_customer_service_enabled:
                    continue
                
                logger.info("Checking for customer messages...")
                
                # Get unanswered messages
                messages = await self.customer_service.get_messages(answered=False)
                
                # Handle each message
                for message in messages:
                    try:
                        result = await self.customer_service.handle_message(message.id)
                        if result.get("status") == "success":
                            logger.info(f"Handled message: {message.id}")
                        else:
                            logger.warning(f"Failed to handle message {message.id}: {result.get('message')}")
                    except Exception as e:
                        logger.error(f"Error handling message {message.id}: {e}")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in customer service loop: {e}")
                await asyncio.sleep(180)
    
    async def _ad_optimization_loop(self):
        """Continuous loop for optimizing ad campaigns."""
        logger.info("Starting ad optimization loop")
        
        while self.running:
            try:
                await asyncio.sleep(3600 * 6)  # Run every 6 hours
                
                if not settings.auto_ad_creation_enabled:
                    continue
                
                logger.info("Running ad optimization...")
                
                # Get all campaigns
                campaigns = await self.ad_manager.list_campaigns()
                
                # Analyze and optimize campaigns
                for campaign in campaigns:
                    # In production, would analyze performance and adjust
                    # For now, just log
                    logger.info(f"Checking campaign: {campaign.name}")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in ad optimization loop: {e}")
                await asyncio.sleep(3600)
    
    async def _create_product_ad(self, product):
        """Auto-create ad campaign for a product."""
        try:
            from backend.models.schemas import AdCampaign, AdPlatform
            
            # Create TikTok campaign
            campaign = AdCampaign(
                name=f"Promote {product.title}",
                platform=AdPlatform.TIKTOK,
                product_id=product.id,
                budget=50.0,
                daily_budget=10.0,
                target_audience={
                    "age_range": [18, 45],
                    "genders": [1, 2],
                    "location": ["US"],
                    "interests": ["shopping", "ecommerce"]
                },
                creative_caption="",
                status="draft"
            )
            
            created = await self.ad_manager.create_campaign(campaign)
            logger.info(f"Created ad campaign: {created.id}")
            
        except Exception as e:
            logger.error(f"Error creating product ad: {e}")

