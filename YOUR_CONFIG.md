# Your Configuration Setup

Based on your provided credentials, here's your `.env` file setup:

## ✅ What You Have

1. **Hugging Face Token**: `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` ✅
2. **CJdropshipping API Key**: `CJ4867432@api@01020a40357c462d9abad2e3fff121f6` ✅
3. **Shopify API Key**: `c1492823ddee84d51e484dec2bed57ad` ✅
4. **Shopify API Secret**: `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` ✅

## 📝 Your `.env` File

Create `config/.env` file with this content:

```env
# Application Settings
DEBUG=False
LOG_LEVEL=INFO

# Shopify Configuration
SHOPIFY_API_KEY=c1492823ddee84d51e484dec2bed57ad
SHOPIFY_API_SECRET=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
SHOPIFY_STORE_NAME=ajneux-ch
SHOPIFY_ACCESS_TOKEN=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

# CJdropshipping Configuration
CJ_API_KEY=CJ4867432@api@01020a40357c462d9abad2e3fff121f6
CJ_API_SECRET=your_cj_api_secret
CJ_BASE_URL=https://api.cjdropshipping.com

# Hugging Face Configuration (instead of OpenAI)
HUGGINGFACE_API_TOKEN=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
HUGGINGFACE_MODEL=meta-llama/Meta-Llama-3-8B-Instruct

# OpenAI (optional - you're using Hugging Face instead)
OPENAI_API_KEY=

# TikTok Ads (optional - can add later)
TIKTOK_CLIENT_ID=
TIKTOK_CLIENT_SECRET=
TIKTOK_ADVERTISER_ID=
TIKTOK_ACCESS_TOKEN=

# Facebook Ads (optional - can add later)
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=
FACEBOOK_ACCESS_TOKEN=
FACEBOOK_AD_ACCOUNT_ID=

# Product Discovery Settings
MIN_PROFIT_MARGIN=0.30
MIN_DAILY_SALES=10
MAX_PRODUCT_PRICE=100.0

# Automation Settings
AUTO_FULFILL_ENABLED=True
AUTO_AD_CREATION_ENABLED=True
AUTO_CUSTOMER_SERVICE_ENABLED=True
```

## 🔧 Next Steps

### 1. Get Shopify Store Name and Access Token

You already have the Client ID and Secret! Now you just need:

**A. Store Name:**
- Check your Shopify admin URL
- Example: If URL is `https://mystore.myshopify.com/admin`, store name is `mystore`
- Or go to Settings → General in Shopify admin

**B. Access Token:**
1. Go to: https://partners.shopify.com
2. Click "Apps" → Find your app (API Key: `c1492823ddee84d51e484dec2bed57ad`)
3. Click on the app
4. Go to "API credentials" tab
5. Look for "Admin API access token"
6. Click "Reveal token once" ⚠️ (Copy immediately - you won't see it again!)
7. This is your `SHOPIFY_ACCESS_TOKEN`

**Note:** Make sure the app is installed on your store first (go to "Overview" tab → "Install app")

### 2. Get CJdropshipping API Secret

1. Go to your CJdropshipping account
2. Navigate to API settings
3. Look for "API Secret" (different from API Key)
4. Copy it to `CJ_API_SECRET` in `.env`

If you can't find the secret, the API key might work alone - try it first!

### 3. Test the System

Once you have Shopify API keys:

```bash
# 1. Create .env file
cp config/.env.example config/.env
# Edit config/.env with your keys

# 2. Start backend
cd backend
python main.py

# 3. Start frontend (new terminal)
cd frontend
npm run dev

# 4. Visit http://localhost:3000
```

## ✅ Quick Checklist

- [ ] Created `config/.env` file
- [ ] Added Hugging Face token ✅
- [ ] Added CJdropshipping API key ✅
- [ ] Got Shopify API keys (from developer dashboard)
- [ ] Got CJdropshipping API secret (if needed)
- [ ] Started the system
- [ ] Tested product discovery
- [ ] Tested store connection

## 🎯 What Works Now

With just Hugging Face + CJdropshipping:
- ✅ AI content generation (using Hugging Face)
- ✅ Product discovery (using CJdropshipping)
- ✅ Mock mode for Shopify (until you add API keys)
- ✅ Mock mode for ads (until you add TikTok/Facebook)

## 💡 Tips

1. **Shopify Development Store**: If you don't have a store yet, create a free development store for testing
2. **CJdropshipping API Secret**: May not be required - try with just the API key first
3. **Hugging Face Model**: The default model should work, but you can change it in `.env` if needed
4. **Testing**: Start with mock mode to test the system before adding all API keys

## 🆘 Need Help?

- See `SETUP_GUIDE.md` for detailed instructions
- Check `docs/SETUP.md` for troubleshooting
- Review error messages in terminal logs

Good luck! 🚀

