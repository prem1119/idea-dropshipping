# Setup Instructions

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL (optional, for production)
- Redis (optional, for Celery tasks)

## Installation

### 1. Backend Setup

```bash
# Navigate to project root
cd "idea dropshipping"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp config/.env.example config/.env

# Edit config/.env with your API keys
# (See Configuration section below)
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# The frontend will proxy API requests to localhost:8000
```

### 3. Configuration

Create `config/.env` file with the following variables:

```env
# Application
DEBUG=False
LOG_LEVEL=INFO

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost/dropshipping

# Shopify
SHOPIFY_API_KEY=your_shopify_api_key
SHOPIFY_API_SECRET=your_shopify_api_secret
SHOPIFY_STORE_NAME=your-store-name
SHOPIFY_ACCESS_TOKEN=your_shopify_access_token

# CJdropshipping
CJ_API_KEY=your_cj_api_key
CJ_API_SECRET=your_cj_api_secret

# TikTok Ads
TIKTOK_CLIENT_ID=your_tiktok_client_id
TIKTOK_CLIENT_SECRET=your_tiktok_client_secret
TIKTOK_ADVERTISER_ID=your_tiktok_advertiser_id
TIKTOK_ACCESS_TOKEN=your_tiktok_access_token

# Facebook Ads
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_AD_ACCOUNT_ID=your_facebook_ad_account_id

# OpenAI (for AI features)
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4-turbo-preview

# Anthropic (Claude - optional)
ANTHROPIC_API_KEY=your_anthropic_api_key

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Automation Settings
MIN_PROFIT_MARGIN=0.30
MIN_DAILY_SALES=10
MAX_PRODUCT_PRICE=100.0
AUTO_FULFILL_ENABLED=True
AUTO_AD_CREATION_ENABLED=True
AUTO_CUSTOMER_SERVICE_ENABLED=True
```

## Running the Application

### Start Backend

```bash
# From project root
cd backend
python main.py

# Or using uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Start Frontend

```bash
# From frontend directory
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Getting API Keys

### Shopify
1. Go to https://partners.shopify.com
2. Create a partner account
3. Create a development store or connect existing store
4. Create a custom app in your store admin
5. Get API credentials from app settings

### CJdropshipping
1. Sign up at https://www.cjdropshipping.com
2. Go to API section in account settings
3. Generate API key and secret

### TikTok Ads
1. Go to https://ads.tiktok.com
2. Create an advertiser account
3. Navigate to Tools > API
4. Create an app and get credentials

### Facebook Ads
1. Go to https://developers.facebook.com
2. Create an app
3. Add Marketing API product
4. Get access tokens from Graph API Explorer

### OpenAI
1. Go to https://platform.openai.com
2. Sign up and add payment method
3. Get API key from API keys section

## Troubleshooting

### Backend won't start
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.10+)
- Check port 8000 is not in use

### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Check port 3000 is not in use

### API errors
- Verify all API keys are correct in `config/.env`
- Check API rate limits
- Review logs for specific error messages

