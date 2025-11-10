"""Application settings and configuration."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Automated Dropshipping System"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://user:pass@localhost/dropshipping"
    
    # Shopify
    shopify_api_key: Optional[str] = None
    shopify_api_secret: Optional[str] = None
    shopify_store_name: Optional[str] = None
    shopify_access_token: Optional[str] = None
    
    # AliExpress API (using CJdropshipping as primary)
    cj_api_key: Optional[str] = None
    cj_api_secret: Optional[str] = None
    cj_base_url: str = "https://api.cjdropshipping.com"
    
    # TikTok Ads
    tiktok_client_id: Optional[str] = None
    tiktok_client_secret: Optional[str] = None
    tiktok_advertiser_id: Optional[str] = None
    tiktok_access_token: Optional[str] = None
    
    # Facebook Ads
    facebook_app_id: Optional[str] = None
    facebook_app_secret: Optional[str] = None
    facebook_access_token: Optional[str] = None
    facebook_ad_account_id: Optional[str] = None
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    
    # Hugging Face (alternative to OpenAI)
    huggingface_api_token: Optional[str] = None
    huggingface_model: str = "meta-llama/Meta-Llama-3-8B-Instruct"  # Or "mistralai/Mistral-7B-Instruct-v0.2"
    
    # Anthropic (Claude)
    anthropic_api_key: Optional[str] = None
    
    # Redis (for Celery)
    redis_url: str = "redis://localhost:6379/0"
    
    # Product Discovery
    min_profit_margin: float = 0.30  # 30% minimum margin
    min_daily_sales: int = 10
    max_product_price: float = 100.0
    
    # Automation
    auto_fulfill_enabled: bool = True
    auto_ad_creation_enabled: bool = True
    auto_customer_service_enabled: bool = True
    
    # Monitoring
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


_settings = None


def get_settings() -> Settings:
    """Get settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

