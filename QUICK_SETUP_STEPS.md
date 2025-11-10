# Quick Setup Steps - Final Checklist ✅

## You Have These Credentials:

✅ **Hugging Face**: `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`  
✅ **CJdropshipping**: `CJ4867432@api@01020a40357c462d9abad2e3fff121f6`  
✅ **Shopify API Key**: `c1492823ddee84d51e484dec2bed57ad`  
✅ **Shopify API Secret**: `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`  

## What You Need to Do:

### 1. Create `.env` File (2 minutes)

```bash
# In project root
cp config/.env.example config/.env
```

### 2. Fill in `.env` File

Open `config/.env` and paste this (replace the placeholders):

```env
SHOPIFY_API_KEY=c1492823ddee84d51e484dec2bed57ad
SHOPIFY_API_SECRET=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
SHOPIFY_STORE_NAME=ajneux-ch
SHOPIFY_ACCESS_TOKEN=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

CJ_API_KEY=CJ4867432@api@01020a40357c462d9abad2e3fff121f6
CJ_BASE_URL=https://api.cjdropshipping.com

HUGGINGFACE_API_TOKEN=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
HUGGINGFACE_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
```

### 3. Get Missing Info (5 minutes)

**A. Store Name:**
- Check your Shopify admin URL
- Example: `https://mystore.myshopify.com/admin` → Store name is `mystore`

**B. Access Token:**
1. Go to: https://partners.shopify.com
2. Click "Apps" → Find your app
3. Click "API credentials" tab
4. Click "Reveal token once" next to "Admin API access token"
5. Copy it immediately!

### 4. Start System

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

### 5. Open Dashboard

Visit: **http://localhost:3000**

---

## That's It! 🎉

See `YOUR_COMPLETE_CONFIG.md` for detailed instructions.

