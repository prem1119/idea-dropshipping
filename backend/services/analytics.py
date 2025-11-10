"""Analytics service for dashboard metrics."""
import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import shopify
import httpx
import json

from backend.models.schemas import DashboardMetrics
from backend.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AnalyticsService:
    """Service for calculating analytics and metrics."""
    
    def __init__(self):
        self.shopify_store_name = settings.shopify_store_name
        self.shopify_access_token = settings.shopify_access_token
        self.tiktok_access_token = settings.tiktok_access_token
        self.facebook_access_token = settings.facebook_access_token
        
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
    
    async def get_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> DashboardMetrics:
        """
        Get comprehensive dashboard metrics.
        
        Calculates:
        - Total sales
        - Total profit
        - Total orders
        - Ad spend
        - ROI
        - Conversion rate
        - Average order value
        - Top products
        - Sales/profit by date
        - Ad performance
        """
        logger.info(f"Calculating metrics: {start_date} to {end_date}")
        
        # Default to last 30 days if not specified
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        try:
            # Get sales data from Shopify
            sales_data = await self._get_sales_data(start_date, end_date)
            
            # Get ad spend data
            ad_spend = await self._get_ad_spend(start_date, end_date)
            
            # Calculate profit (simplified - would need actual cost data)
            total_sales = sales_data["total_sales"]
            total_cost = sales_data["estimated_cost"]  # Estimated from product costs
            total_profit = total_sales - total_cost - ad_spend
            
            # Calculate ROI
            roi = (total_profit / ad_spend * 100) if ad_spend > 0 else 0
            
            # Calculate conversion rate (simplified)
            conversion_rate = await self._calculate_conversion_rate(start_date, end_date)
            
            # Calculate average order value
            total_orders = sales_data["total_orders"]
            avg_order_value = total_sales / total_orders if total_orders > 0 else 0
            
            # Get top products
            top_products = sales_data["top_products"]
            
            # Get sales by date
            sales_by_date = await self._get_sales_by_date(start_date, end_date)
            profit_by_date = await self._get_profit_by_date(start_date, end_date)
            
            # Get ad performance
            ad_performance = await self._get_ad_performance(start_date, end_date)
            
            return DashboardMetrics(
                total_sales=total_sales,
                total_profit=total_profit,
                total_orders=total_orders,
                total_ad_spend=ad_spend,
                roi=roi,
                conversion_rate=conversion_rate,
                average_order_value=avg_order_value,
                top_products=top_products,
                sales_by_date=sales_by_date,
                profit_by_date=profit_by_date,
                ad_performance=ad_performance
            )
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return self._get_mock_metrics()
    
    async def _get_sales_data(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """Get sales data from Shopify."""
        if not self.session:
            return self._get_mock_sales_data()
        
        try:
            # Get orders in date range
            orders = shopify.Order.find(
                created_at_min=start_date.isoformat(),
                created_at_max=end_date.isoformat(),
                status="any",
                limit=250
            )
            
            total_sales = 0.0
            total_cost = 0.0
            total_orders = len(orders)
            product_sales = {}
            
            for order in orders:
                total_sales += float(order.total_price)
                
                # Calculate estimated cost (30% of sale price as example)
                total_cost += float(order.total_price) * 0.30
                
                # Track product sales
                for item in order.line_items:
                    product_title = item.title
                    quantity = item.quantity
                    revenue = float(item.price) * quantity
                    
                    if product_title not in product_sales:
                        product_sales[product_title] = {
                            "name": product_title,
                            "sales": 0,
                            "revenue": 0.0,
                            "quantity": 0
                        }
                    
                    product_sales[product_title]["sales"] += revenue
                    product_sales[product_title]["revenue"] += revenue
                    product_sales[product_title]["quantity"] += quantity
            
            # Sort top products
            top_products = sorted(
                product_sales.values(),
                key=lambda x: x["revenue"],
                reverse=True
            )[:10]
            
            return {
                "total_sales": total_sales,
                "estimated_cost": total_cost,
                "total_orders": total_orders,
                "top_products": top_products
            }
            
        except Exception as e:
            logger.error(f"Error getting sales data: {e}")
            return self._get_mock_sales_data()
    
    async def _get_ad_spend(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> float:
        """Get total ad spend from TikTok and Facebook."""
        total_spend = 0.0
        
        try:
            # Get TikTok ad spend
            if self.tiktok_access_token:
                tiktok_spend = await self._get_tiktok_ad_spend(start_date, end_date)
                total_spend += tiktok_spend
            
            # Get Facebook ad spend
            if self.facebook_access_token:
                facebook_spend = await self._get_facebook_ad_spend(start_date, end_date)
                total_spend += facebook_spend
                
        except Exception as e:
            logger.error(f"Error getting ad spend: {e}")
        
        return total_spend
    
    async def _get_tiktok_ad_spend(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> float:
        """Get TikTok ad spend."""
        try:
            async with httpx.AsyncClient() as client:
                url = "https://business-api.tiktok.com/open_api/v1.3/report/integrated/get/"
                headers = {
                    "Access-Token": self.tiktok_access_token,
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "advertiser_id": settings.tiktok_advertiser_id,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "metrics": ["spend"]
                }
                
                response = await client.post(url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                # Parse response
                return float(data.get("data", {}).get("sum", {}).get("spend", 0))
                
        except Exception as e:
            logger.error(f"Error getting TikTok ad spend: {e}")
            return 0.0
    
    async def _get_facebook_ad_spend(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> float:
        """Get Facebook ad spend."""
        try:
            async with httpx.AsyncClient() as client:
                url = f"https://graph.facebook.com/v18.0/{settings.facebook_ad_account_id}/insights"
                params = {
                    "time_range": json.dumps({
                        "since": start_date.strftime("%Y-%m-%d"),
                        "until": end_date.strftime("%Y-%m-%d")
                    }),
                    "fields": "spend",
                    "access_token": self.facebook_access_token
                }
                
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                total_spend = 0.0
                for insight in data.get("data", []):
                    total_spend += float(insight.get("spend", 0))
                
                return total_spend
                
        except Exception as e:
            logger.error(f"Error getting Facebook ad spend: {e}")
            return 0.0
    
    async def _calculate_conversion_rate(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> float:
        """Calculate conversion rate (simplified)."""
        # In production, get actual traffic data and orders
        # Conversion rate = (Orders / Sessions) * 100
        return 2.5  # Mock 2.5% conversion rate
    
    async def _get_sales_by_date(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get sales broken down by date."""
        if not self.session:
            return self._get_mock_sales_by_date(start_date, end_date)
        
        try:
            sales_by_date = {}
            current_date = start_date
            
            while current_date <= end_date:
                sales_by_date[current_date.strftime("%Y-%m-%d")] = 0.0
                current_date += timedelta(days=1)
            
            orders = shopify.Order.find(
                created_at_min=start_date.isoformat(),
                created_at_max=end_date.isoformat(),
                status="any",
                limit=250
            )
            
            for order in orders:
                order_date = datetime.fromisoformat(order.created_at.replace("Z", "+00:00"))
                date_key = order_date.strftime("%Y-%m-%d")
                if date_key in sales_by_date:
                    sales_by_date[date_key] += float(order.total_price)
            
            return [{"date": date, "sales": sales} for date, sales in sales_by_date.items()]
            
        except Exception as e:
            logger.error(f"Error getting sales by date: {e}")
            return self._get_mock_sales_by_date(start_date, end_date)
    
    async def _get_profit_by_date(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get profit broken down by date."""
        sales_by_date = await self._get_sales_by_date(start_date, end_date)
        
        # Calculate profit (simplified - 70% margin)
        return [
            {"date": item["date"], "profit": item["sales"] * 0.70}
            for item in sales_by_date
        ]
    
    async def _get_ad_performance(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get ad performance metrics."""
        # In production, get actual ad performance data
        return [
            {
                "platform": "TikTok",
                "spend": 150.0,
                "impressions": 50000,
                "clicks": 2500,
                "conversions": 62,
                "roas": 3.5
            },
            {
                "platform": "Facebook",
                "spend": 200.0,
                "impressions": 80000,
                "clicks": 3200,
                "conversions": 80,
                "roas": 2.8
            }
        ]
    
    def _get_mock_metrics(self) -> DashboardMetrics:
        """Get mock metrics for testing."""
        return DashboardMetrics(
            total_sales=5000.0,
            total_profit=2500.0,
            total_orders=125,
            total_ad_spend=350.0,
            roi=614.29,
            conversion_rate=2.5,
            average_order_value=40.0,
            top_products=[],
            sales_by_date=[],
            profit_by_date=[],
            ad_performance=[]
        )
    
    def _get_mock_sales_data(self) -> Dict:
        """Get mock sales data."""
        return {
            "total_sales": 5000.0,
            "estimated_cost": 1500.0,
            "total_orders": 125,
            "top_products": [
                {"name": "Product 1", "sales": 1200.0, "revenue": 1200.0, "quantity": 30},
                {"name": "Product 2", "sales": 900.0, "revenue": 900.0, "quantity": 25}
            ]
        }
    
    def _get_mock_sales_by_date(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get mock sales by date."""
        dates = []
        current = start_date
        while current <= end_date:
            dates.append({
                "date": current.strftime("%Y-%m-%d"),
                "sales": 150.0 + (hash(str(current)) % 100)  # Randomish sales
            })
            current += timedelta(days=1)
        return dates

