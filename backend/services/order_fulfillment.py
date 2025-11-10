"""Order fulfillment service for automatic order processing."""
import logging
from typing import List, Optional, Dict
from datetime import datetime
import httpx
import shopify

from backend.models.schemas import Order
from backend.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class OrderFulfillmentService:
    """Service for automatic order fulfillment."""
    
    def __init__(self):
        self.cj_api_key = settings.cj_api_key
        self.cj_api_secret = settings.cj_api_secret
        self.cj_base_url = settings.cj_base_url
        self.shopify_access_token = settings.shopify_access_token
        self.shopify_store_name = settings.shopify_store_name
        self.auto_fulfill_enabled = settings.auto_fulfill_enabled
        
        # Initialize Shopify session
        if self.shopify_store_name and self.shopify_access_token:
            shopify.ShopifyResource.set_site(
                f"https://{self.shopify_store_name}.myshopify.com/admin/api/2024-01"
            )
            self.session = shopify.Session(
                f"{self.shopify_store_name}.myshopify.com",
                "2024-01",
                self.shopify_access_token
            )
        else:
            self.session = None
    
    async def get_pending_orders(self) -> List[Order]:
        """Get all pending orders that need fulfillment."""
        if not self.session:
            logger.warning("Shopify not configured, returning mock orders")
            return self._get_mock_orders()
        
        try:
            # Get unfulfilled orders
            orders = shopify.Order.find(
                fulfillment_status="unfulfilled",
                status="any",
                limit=50
            )
            
            order_list = []
            for shopify_order in orders:
                order = Order(
                    id=str(shopify_order.id),
                    order_number=shopify_order.order_number,
                    customer_name=f"{shopify_order.customer.first_name} {shopify_order.customer.last_name}",
                    customer_email=shopify_order.customer.email,
                    items=[{
                        "title": item.title,
                        "quantity": item.quantity,
                        "price": float(item.price),
                        "sku": item.sku
                    } for item in shopify_order.line_items],
                    total=float(shopify_order.total_price),
                    currency=shopify_order.currency,
                    shipping_address={
                        "name": shopify_order.shipping_address.name,
                        "address1": shopify_order.shipping_address.address1,
                        "city": shopify_order.shipping_address.city,
                        "province": shopify_order.shipping_address.province,
                        "zip": shopify_order.shipping_address.zip,
                        "country": shopify_order.shipping_address.country
                    },
                    status=shopify_order.financial_status,
                    fulfillment_status=shopify_order.fulfillment_status,
                    created_at=shopify_order.created_at
                )
                order_list.append(order)
            
            return order_list
            
        except Exception as e:
            logger.error(f"Error getting pending orders: {e}")
            return []
    
    async def fulfill_order(self, order_id: str) -> Dict:
        """
        Automatically fulfill an order through CJdropshipping.
        Creates fulfillment request and updates tracking.
        """
        logger.info(f"Fulfilling order: {order_id}")
        
        if not self.auto_fulfill_enabled:
            return {"status": "disabled", "message": "Auto-fulfillment is disabled"}
        
        try:
            # Get order from Shopify
            if not self.session:
                return {"status": "error", "message": "Shopify not configured"}
            
            shopify_order = shopify.Order.find(order_id)
            
            # Extract order details
            items = []
            for line_item in shopify_order.line_items:
                items.append({
                    "sku": line_item.sku,
                    "quantity": line_item.quantity
                })
            
            shipping_address = shopify_order.shipping_address
            
            # Create fulfillment request with CJdropshipping
            fulfillment_result = await self._create_cj_fulfillment(
                order_id=order_id,
                items=items,
                shipping_address=shipping_address
            )
            
            if fulfillment_result.get("success"):
                # Update Shopify order with tracking
                tracking_number = fulfillment_result.get("tracking_number")
                
                # Create fulfillment in Shopify
                fulfillment = shopify.Fulfillment()
                fulfillment.order_id = order_id
                fulfillment.tracking_number = tracking_number
                fulfillment.tracking_company = "CJ Logistics"
                fulfillment.tracking_urls = [fulfillment_result.get("tracking_url", "")]
                
                if fulfillment.save():
                    logger.info(f"Order {order_id} fulfilled successfully")
                    return {
                        "status": "success",
                        "order_id": order_id,
                        "tracking_number": tracking_number,
                        "tracking_url": fulfillment_result.get("tracking_url")
                    }
                else:
                    logger.error(f"Failed to update Shopify fulfillment: {fulfillment.errors}")
                    return {"status": "partial", "message": "Order fulfilled but Shopify update failed"}
            
            return {"status": "error", "message": fulfillment_result.get("error")}
            
        except Exception as e:
            logger.error(f"Error fulfilling order {order_id}: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _create_cj_fulfillment(
        self,
        order_id: str,
        items: List[Dict],
        shipping_address: Dict
    ) -> Dict:
        """Create fulfillment request with CJdropshipping."""
        if not self.cj_api_key:
            logger.warning("CJ API not configured, returning mock fulfillment")
            return {
                "success": True,
                "tracking_number": f"CJ{order_id[:8]}",
                "tracking_url": f"https://tracking.cjdropshipping.com/{order_id}"
            }
        
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.cj_base_url}/api/orders/create"
                headers = {
                    "Authorization": f"Bearer {self.cj_api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "order_id": order_id,
                    "items": items,
                    "shipping": {
                        "name": shipping_address.get("name"),
                        "address": shipping_address.get("address1"),
                        "city": shipping_address.get("city"),
                        "state": shipping_address.get("province"),
                        "zip": shipping_address.get("zip"),
                        "country": shipping_address.get("country")
                    },
                    "shipping_method": "standard"  # or "express" based on customer selection
                }
                
                response = await client.post(url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "success": True,
                    "tracking_number": data.get("tracking_number"),
                    "tracking_url": data.get("tracking_url"),
                    "estimated_delivery": data.get("estimated_delivery")
                }
                
        except Exception as e:
            logger.error(f"Error creating CJ fulfillment: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_tracking(self, order_id: str, tracking_number: str) -> bool:
        """Update tracking information for an order."""
        if not self.session:
            return False
        
        try:
            order = shopify.Order.find(order_id)
            fulfillments = shopify.Fulfillment.find(order_id=order_id)
            
            if fulfillments:
                fulfillment = fulfillments[0]
                fulfillment.tracking_number = tracking_number
                return fulfillment.save()
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating tracking: {e}")
            return False
    
    def _get_mock_orders(self) -> List[Order]:
        """Get mock orders for testing."""
        return [
            Order(
                id="order-001",
                order_number="#1001",
                customer_name="John Doe",
                customer_email="john@example.com",
                items=[{"title": "Product 1", "quantity": 2, "price": 29.99}],
                total=59.98,
                currency="USD",
                shipping_address={
                    "name": "John Doe",
                    "address1": "123 Main St",
                    "city": "New York",
                    "province": "NY",
                    "zip": "10001",
                    "country": "US"
                },
                status="paid",
                fulfillment_status="unfulfilled",
                created_at=datetime.utcnow()
            )
        ]

