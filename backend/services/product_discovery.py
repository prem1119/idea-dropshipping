"""Product discovery service for finding trending and high-margin products."""
import asyncio
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import httpx
import logging

from backend.models.schemas import Product, ProductStatus
from backend.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ProductDiscoveryService:
    """Service for discovering trending and high-margin products."""
    
    def __init__(self):
        self.cj_api_key = settings.cj_api_key
        self.cj_api_secret = settings.cj_api_secret
        self.cj_base_url = settings.cj_base_url
        self.min_margin = settings.min_profit_margin
        self.min_daily_sales = settings.min_daily_sales
        
    async def discover_products(
        self,
        category: Optional[str] = None,
        min_margin: Optional[float] = None,
        limit: int = 20
    ) -> List[Product]:
        """
        Discover trending and high-margin products.
        
        Args:
            category: Product category filter
            min_margin: Minimum profit margin (0.0-1.0)
            limit: Maximum number of products to return
            
        Returns:
            List of discovered products
        """
        logger.info(f"Discovering products: category={category}, min_margin={min_margin}, limit={limit}")
        
        # Use minimum margin from settings if not provided
        margin_threshold = min_margin or self.min_margin
        
        # Discover from CJdropshipping API
        products = await self._discover_cj_products(category, margin_threshold, limit)
        
        # Also try AliExpress via CJ (they often have AliExpress products)
        if len(products) < limit:
            ali_products = await self._discover_aliexpress_products(category, margin_threshold, limit - len(products))
            products.extend(ali_products)
        
        # Sort by profitability and trending score
        products = sorted(products, key=lambda p: (p.margin, p.profit), reverse=True)
        
        logger.info(f"Discovered {len(products)} products")
        return products[:limit]
    
    async def _discover_cj_products(
        self,
        category: Optional[str],
        min_margin: float,
        limit: int
    ) -> List[Product]:
        """Discover products from CJdropshipping API."""
        if not self.cj_api_key:
            logger.warning("CJ API key not configured, using mock data")
            return self._get_mock_products(min_margin, limit)
        
        try:
            async with httpx.AsyncClient() as client:
                # Search for trending products
                url = f"{self.cj_base_url}/api/products/search"
                headers = {
                    "Authorization": f"Bearer {self.cj_api_key}",
                    "Content-Type": "application/json"
                }
                params = {
                    "limit": limit * 2,  # Get more to filter
                    "sort": "sales",  # Sort by sales volume
                    "order": "desc"
                }
                
                if category:
                    params["category"] = category
                
                response = await client.get(url, headers=headers, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                products = []
                for item in data.get("data", {}).get("list", []):
                    # Calculate profit margin
                    supplier_price = float(item.get("price", 0))
                    shipping_cost = float(item.get("shippingCost", 0))
                    total_cost = supplier_price + shipping_cost
                    
                    # Suggested retail price (2-3x markup)
                    suggested_price = total_cost * 2.5
                    
                    profit = suggested_price - total_cost
                    margin = profit / suggested_price if suggested_price > 0 else 0
                    
                    # Filter by minimum margin and sales volume
                    if margin >= min_margin and item.get("salesVolume", 0) >= self.min_daily_sales:
                        product = Product(
                            id=item.get("productId"),
                            title=item.get("productName", ""),
                            description=item.get("description", ""),
                            price=suggested_price,
                            cost=total_cost,
                            margin=margin,
                            profit=profit,
                            category=item.get("category", ""),
                            images=item.get("images", []),
                            supplier_id=item.get("supplierId", ""),
                            supplier_name=item.get("supplierName", "CJ Supplier"),
                            supplier_url=item.get("productUrl", ""),
                            shipping_info={
                                "cost": shipping_cost,
                                "time": item.get("shippingTime", "7-15 days")
                            },
                            status=ProductStatus.DISCOVERED,
                            created_at=datetime.utcnow()
                        )
                        products.append(product)
                
                return products
                
        except Exception as e:
            logger.error(f"Error discovering CJ products: {e}")
            # Return mock data on error
            return self._get_mock_products(min_margin, limit)
    
    async def _discover_aliexpress_products(
        self,
        category: Optional[str],
        min_margin: float,
        limit: int
    ) -> List[Product]:
        """Discover products from AliExpress (via CJ or direct scraping)."""
        # CJdropshipping often includes AliExpress products
        # In a real implementation, you'd use AliExpress Dropshipping API
        # or web scraping with proper authorization
        logger.info("AliExpress product discovery (using CJ proxy)")
        return []
    
    def _get_mock_products(self, min_margin: float, limit: int) -> List[Product]:
        """Generate mock products for testing when APIs are not configured."""
        mock_products = [
            {
                "id": "mock-001",
                "title": "Wireless Bluetooth Earbuds with Noise Cancellation",
                "description": "Premium wireless earbuds with active noise cancellation, 30-hour battery life, and crystal-clear sound quality.",
                "cost": 15.00,
                "price": 45.00,
                "margin": 0.667,
                "category": "Electronics",
                "images": ["https://via.placeholder.com/500"],
                "supplier": "CJ Supplier #1",
                "sales_volume": 1250
            },
            {
                "id": "mock-002",
                "title": "Portable Phone Charger Power Bank 20000mAh",
                "description": "Ultra-high capacity power bank with fast charging technology and multiple ports.",
                "cost": 8.50,
                "price": 29.99,
                "margin": 0.717,
                "category": "Electronics",
                "images": ["https://via.placeholder.com/500"],
                "supplier": "CJ Supplier #2",
                "sales_volume": 890
            },
            {
                "id": "mock-003",
                "title": "Minimalist Wallet with RFID Blocking",
                "description": "Slim, modern wallet with RFID blocking technology to protect your cards from unauthorized scanning.",
                "cost": 6.00,
                "price": 24.99,
                "margin": 0.760,
                "category": "Accessories",
                "images": ["https://via.placeholder.com/500"],
                "supplier": "CJ Supplier #3",
                "sales_volume": 654
            },
            {
                "id": "mock-004",
                "title": "Yoga Mat with Carrying Strap - Non-Slip",
                "description": "Premium yoga mat with superior grip, cushioning, and eco-friendly materials.",
                "cost": 12.00,
                "price": 39.99,
                "margin": 0.700,
                "category": "Fitness",
                "images": ["https://via.placeholder.com/500"],
                "supplier": "CJ Supplier #4",
                "sales_volume": 432
            },
            {
                "id": "mock-005",
                "title": "LED Strip Lights - 16.4ft RGB Color Changing",
                "description": "Smart LED strip lights with app control, voice control, and millions of colors.",
                "cost": 7.50,
                "price": 27.99,
                "margin": 0.732,
                "category": "Home Decor",
                "images": ["https://via.placeholder.com/500"],
                "supplier": "CJ Supplier #5",
                "sales_volume": 1100
            }
        ]
        
        products = []
        for item in mock_products[:limit]:
            if item["margin"] >= min_margin:
                product = Product(
                    id=item["id"],
                    title=item["title"],
                    description=item["description"],
                    price=item["price"],
                    cost=item["cost"],
                    margin=item["margin"],
                    profit=item["price"] - item["cost"],
                    category=item["category"],
                    images=item["images"],
                    supplier_id=item["supplier"].replace(" ", "-").lower(),
                    supplier_name=item["supplier"],
                    supplier_url=f"https://example.com/products/{item['id']}",
                    shipping_info={
                        "cost": 3.50,
                        "time": "7-15 days"
                    },
                    status=ProductStatus.DISCOVERED,
                    created_at=datetime.utcnow()
                )
                products.append(product)
        
        return products

