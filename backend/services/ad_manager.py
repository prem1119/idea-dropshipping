"""Ad campaign management service for TikTok and Facebook."""
import logging
from typing import List, Optional, Dict
import httpx
from datetime import datetime

from backend.models.schemas import AdCampaign, AdPlatform
from backend.config.settings import get_settings
from backend.services.ai_content_generator import AIContentGenerator
from backend.services.video_generator import VideoGenerator

logger = logging.getLogger(__name__)
settings = get_settings()


class AdManager:
    """Service for managing TikTok and Facebook ad campaigns."""
    
    def __init__(self):
        self.tiktok_access_token = settings.tiktok_access_token
        self.tiktok_advertiser_id = settings.tiktok_advertiser_id
        self.facebook_access_token = settings.facebook_access_token
        self.facebook_ad_account_id = settings.facebook_ad_account_id
        self.content_generator = AIContentGenerator()
        self.video_generator = VideoGenerator()
    
    async def create_campaign(self, campaign: AdCampaign) -> AdCampaign:
        """
        Create an ad campaign on TikTok or Facebook.
        Generates video and caption automatically if not provided.
        """
        logger.info(f"Creating ad campaign: {campaign.name} on {campaign.platform}")
        
        # Generate caption if not provided
        if not campaign.creative_caption:
            # Get product info (would normally fetch from database)
            product_title = campaign.name  # Simplified
            caption = await self.content_generator.generate_ad_caption(
                product_title,
                "",
                campaign.platform.value
            )
            campaign.creative_caption = caption
        
        # Generate video if not provided
        if not campaign.creative_video_url:
            video_url = await self._generate_video_ad(campaign)
            if video_url:
                campaign.creative_video_url = video_url
        
        # Create campaign on platform
        if campaign.platform == AdPlatform.TIKTOK:
            result = await self._create_tiktok_campaign(campaign)
        elif campaign.platform == AdPlatform.FACEBOOK:
            result = await self._create_facebook_campaign(campaign)
        else:
            raise ValueError(f"Unsupported platform: {campaign.platform}")
        
        campaign.id = result.get("campaign_id")
        campaign.status = result.get("status", "active")
        campaign.created_at = datetime.utcnow()
        
        return campaign
    
    async def _generate_video_ad(self, campaign: AdCampaign) -> Optional[str]:
        """Generate video ad using AI video generation."""
        try:
            # Get product info (simplified - would fetch from DB in production)
            product_title = campaign.name
            
            # Generate video script
            script = await self.content_generator.generate_video_script(
                product_title,
                "",
                15
            )
            
            # Generate video using video generator service
            video_url = await self.video_generator.generate_product_video(
                product_title=product_title,
                script=script,
                duration_seconds=15
            )
            
            return video_url
            
        except Exception as e:
            logger.error(f"Error generating video ad: {e}")
            return None
    
    async def _create_tiktok_campaign(self, campaign: AdCampaign) -> Dict:
        """Create campaign on TikTok Ads."""
        if not self.tiktok_access_token:
            logger.warning("TikTok API not configured, returning mock campaign")
            return {
                "campaign_id": f"tiktok-{campaign.id or 'mock'}",
                "status": "active",
                "message": "Mock campaign created"
            }
        
        try:
            async with httpx.AsyncClient() as client:
                # TikTok Ads API endpoint
                url = "https://business-api.tiktok.com/open_api/v1.3/ad/campaign/create/"
                headers = {
                    "Access-Token": self.tiktok_access_token,
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "advertiser_id": self.tiktok_advertiser_id,
                    "campaign_name": campaign.name,
                    "budget_mode": "BUDGET_MODE_DAILY" if campaign.daily_budget else "BUDGET_MODE_TOTAL",
                    "budget": campaign.daily_budget or campaign.budget,
                    "objective_type": "CONVERSIONS",
                    "targeting": campaign.target_audience
                }
                
                response = await client.post(url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                # Create ad group and creative
                campaign_id = data.get("data", {}).get("campaign_id")
                if campaign_id:
                    # Create ad group
                    ad_group_result = await self._create_tiktok_ad_group(
                        campaign_id, campaign
                    )
                    
                    return {
                        "campaign_id": campaign_id,
                        "ad_group_id": ad_group_result.get("ad_group_id"),
                        "status": "active"
                    }
                
                return {"campaign_id": campaign_id, "status": "pending"}
                
        except Exception as e:
            logger.error(f"Error creating TikTok campaign: {e}")
            return {"campaign_id": None, "status": "error", "error": str(e)}
    
    async def _create_tiktok_ad_group(
        self,
        campaign_id: str,
        campaign: AdCampaign
    ) -> Dict:
        """Create ad group within TikTok campaign."""
        try:
            async with httpx.AsyncClient() as client:
                url = "https://business-api.tiktok.com/open_api/v1.3/ad/group/create/"
                headers = {
                    "Access-Token": self.tiktok_access_token,
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "advertiser_id": self.tiktok_advertiser_id,
                    "campaign_id": campaign_id,
                    "ad_group_name": f"{campaign.name} - Ad Group",
                    "placement_type": ["PLACEMENT_TIKTOK"],
                    "optimization_goal": "CONVERSION",
                    "budget_mode": "BUDGET_MODE_DAILY",
                    "budget": campaign.daily_budget or (campaign.budget / 7),  # Daily budget
                    "bid_type": "BID_TYPE_NO_BID",
                    "targeting": campaign.target_audience or {
                        "age_range": [18, 55],
                        "genders": [1, 2],  # Both genders
                        "location": ["US"]
                    },
                    "creative": {
                        "video_id": campaign.creative_video_url,  # Would need to upload video first
                        "caption": campaign.creative_caption
                    }
                }
                
                response = await client.post(url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "ad_group_id": data.get("data", {}).get("ad_group_id")
                }
                
        except Exception as e:
            logger.error(f"Error creating TikTok ad group: {e}")
            return {"ad_group_id": None}
    
    async def _create_facebook_campaign(self, campaign: AdCampaign) -> Dict:
        """Create campaign on Facebook Ads."""
        if not self.facebook_access_token:
            logger.warning("Facebook API not configured, returning mock campaign")
            return {
                "campaign_id": f"fb-{campaign.id or 'mock'}",
                "status": "active",
                "message": "Mock campaign created"
            }
        
        try:
            async with httpx.AsyncClient() as client:
                # Create campaign
                url = f"https://graph.facebook.com/v18.0/{self.facebook_ad_account_id}/campaigns"
                params = {
                    "name": campaign.name,
                    "objective": "CONVERSIONS",
                    "status": "PAUSED",  # Start paused, activate manually
                    "special_ad_categories": [],
                    "access_token": self.facebook_access_token
                }
                
                response = await client.post(url, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                campaign_id = data.get("id")
                
                # Create ad set
                ad_set_id = await self._create_facebook_ad_set(
                    campaign_id, campaign
                )
                
                return {
                    "campaign_id": campaign_id,
                    "ad_set_id": ad_set_id,
                    "status": "paused"  # Needs manual activation
                }
                
        except Exception as e:
            logger.error(f"Error creating Facebook campaign: {e}")
            return {"campaign_id": None, "status": "error", "error": str(e)}
    
    async def _create_facebook_ad_set(
        self,
        campaign_id: str,
        campaign: AdCampaign
    ) -> Optional[str]:
        """Create ad set within Facebook campaign."""
        try:
            async with httpx.AsyncClient() as client:
                url = f"https://graph.facebook.com/v18.0/{self.facebook_ad_account_id}/adsets"
                params = {
                    "name": f"{campaign.name} - Ad Set",
                    "campaign_id": campaign_id,
                    "daily_budget": int((campaign.daily_budget or campaign.budget / 7) * 100),  # In cents
                    "billing_event": "IMPRESSIONS",
                    "optimization_goal": "OFFSITE_CONVERSIONS",
                    "targeting": str(campaign.target_audience or {
                        "age_min": 18,
                        "age_max": 55,
                        "genders": [1, 2],
                        "geo_locations": {"countries": ["US"]}
                    }),
                    "status": "PAUSED",
                    "access_token": self.facebook_access_token
                }
                
                response = await client.post(url, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                return data.get("id")
                
        except Exception as e:
            logger.error(f"Error creating Facebook ad set: {e}")
            return None
    
    async def list_campaigns(self) -> List[AdCampaign]:
        """List all ad campaigns."""
        # Would fetch from database in production
        return []

