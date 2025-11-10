"""Shopify store management service."""
import logging
from typing import List, Optional, Dict
import httpx
import json

from backend.models.schemas import Product, StoreConfig
from backend.config.settings import get_settings
from backend.services.ai_content_generator import AIContentGenerator

logger = logging.getLogger(__name__)
settings = get_settings()


class ShopifyManager:
    """Service for managing Shopify store operations."""
    
    def __init__(self):
        self.api_key = settings.shopify_api_key
        self.api_secret = settings.shopify_api_secret
        self.store_name = settings.shopify_store_name
        self.access_token = settings.shopify_access_token
        self.content_generator = AIContentGenerator()
        
        # Shopify API base URL
        if self.store_name and self.access_token:
            self.api_base_url = f"https://{self.store_name}.myshopify.com/admin/api/2024-01"
            self.headers = {
                "X-Shopify-Access-Token": self.access_token,
                "Content-Type": "application/json"
            }
            self.session_configured = True
        else:
            self.api_base_url = None
            self.headers = None
            self.session_configured = False
            logger.warning("Shopify credentials not configured, using mock mode")
    
    async def create_store(self, config: StoreConfig) -> Dict:
        """
        Create or configure a Shopify store.
        
        Note: Store creation requires manual setup through Shopify admin.
        This method configures an existing store.
        """
        if not self.session_configured:
            logger.warning("Shopify not configured, returning mock store")
            return {
                "status": "success",
                "store_url": f"https://{config.store_name}.myshopify.com",
                "message": "Store configured (mock mode)"
            }
        
        try:
            # In a real implementation, you would:
            # 1. Configure store settings (payment, shipping, etc.)
            # 2. Set up themes
            # 3. Configure branding
            # 4. Set up automation rules
            
            logger.info(f"Configuring store: {config.store_name}")
            
            # Store configuration would go here
            # Shopify API calls for store settings
            
            return {
                "status": "success",
                "store_url": config.store_url,
                "store_name": config.store_name,
                "brand_name": config.brand_name
            }
        except Exception as e:
            logger.error(f"Error creating store: {e}")
            raise
    
    async def add_product(self, product: Product) -> Dict:
        """
        Add a product to Shopify store with AI-generated descriptions and branding.
        """
        logger.info(f"Adding product to store: {product.title}")
        
        # Generate enhanced product description using AI
        enhanced_description = await self.content_generator.generate_product_description(
            product_title=product.title,
            base_description=product.description,
            category=product.category
        )
        
        # Generate SEO-optimized title
        seo_title = await self.content_generator.generate_seo_title(product.title)
        
        # Generate product tags
        tags = await self.content_generator.generate_product_tags(
            product.title,
            product.category
        )
        
        if not self.session_configured:
            # Mock mode
            return {
                "id": f"shopify-{product.id}",
                "title": seo_title,
                "description": enhanced_description,
                "price": product.price,
                "status": "active",
                "tags": tags,
                "mock": True
            }
        
        try:
            # Prepare product data for Shopify API
            product_data = {
                "product": {
                    "title": seo_title,
                    "body_html": enhanced_description,
                    "vendor": product.supplier_name,
                    "product_type": product.category,
                    "tags": tags,
                    "variants": [{
                        "price": str(product.price),
                        "sku": product.id,
                        "inventory_quantity": 100,
                        "inventory_management": "shopify"
                    }],
                    "images": [{"src": img_url} for img_url in product.images[:5]]  # Limit to 5 images
                }
            }
            
            # Create product via Shopify REST API
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.api_base_url}/products.json"
                response = await client.post(url, headers=self.headers, json=product_data)
                response.raise_for_status()
                
                result = response.json()
                shopify_product = result["product"]
                
                logger.info(f"Product added successfully: {shopify_product['id']}")
                return {
                    "id": str(shopify_product["id"]),
                    "title": shopify_product["title"],
                    "description": shopify_product.get("body_html", ""),
                    "price": float(shopify_product["variants"][0]["price"]) if shopify_product.get("variants") else product.price,
                    "status": shopify_product.get("status", "active"),
                    "tags": shopify_product.get("tags", "").split(",") if shopify_product.get("tags") else tags,
                    "url": f"https://{self.store_name}.myshopify.com/products/{shopify_product.get('handle', '')}"
                }
                
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            raise
    
    async def get_products(self, limit: int = 50) -> List[Dict]:
        """Get all products from store."""
        if not self.session_configured:
            return []
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.api_base_url}/products.json?limit={limit}"
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                
                result = response.json()
                products = result.get("products", [])
                return [self._serialize_product(p) for p in products]
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            return []
    
    async def update_product_price(self, product_id: str, new_price: float) -> bool:
        """Update product price."""
        if not self.session_configured:
            return False
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Get product first to get variant ID
                url = f"{self.api_base_url}/products/{product_id}.json"
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                
                product = response.json()["product"]
                if product.get("variants"):
                    variant_id = product["variants"][0]["id"]
                    # Update variant price
                    update_url = f"{self.api_base_url}/variants/{variant_id}.json"
                    update_data = {"variant": {"price": str(new_price)}}
                    update_response = await client.put(update_url, headers=self.headers, json=update_data)
                    update_response.raise_for_status()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating price: {e}")
            return False
    
    def _serialize_product(self, shopify_product: Dict) -> Dict:
        """Serialize Shopify product to dict."""
        return {
            "id": str(shopify_product.get("id", "")),
            "title": shopify_product.get("title", ""),
            "description": shopify_product.get("body_html", ""),
            "price": float(shopify_product["variants"][0]["price"]) if shopify_product.get("variants") else 0,
            "status": shopify_product.get("status", "active"),
            "url": f"https://{self.store_name}.myshopify.com/products/{shopify_product.get('handle', '')}"
        }

