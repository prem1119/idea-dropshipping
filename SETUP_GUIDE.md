# Complete Setup Guide - Websites to Sign Up For

## 📋 Quick Checklist

Here are all the websites you need to sign up for to get your automated dropshipping system running:

### ✅ ESSENTIAL (Minimum Required)
1. [ ] **Shopify** - For your online store
2. [ ] **CJdropshipping** OR **AliExpress** - For product sourcing
3. [ ] **OpenAI** - For AI features (descriptions, customer service)

### ⭐ RECOMMENDED (For Full Automation)
4. [ ] **TikTok Ads** - For automated ad campaigns
5. [ ] **Facebook Ads** - For automated ad campaigns

### 📝 NOTES
- The system works in **mock mode** for testing WITHOUT all accounts
- You can start with just Shopify and test everything else later
- Each account is free to create (some require payment for API usage)

---

## 1. Shopify Account ⭐ ESSENTIAL

**Website:** https://www.shopify.com

**Steps:**
1. Go to https://www.shopify.com
2. Click **"Start free trial"**
3. Enter your email and create password
4. Answer the business questions (or skip)
5. Choose your store name
6. Complete the setup wizard

**Getting API Credentials:**
1. Go to your Shopify Admin: `https://[your-store-name].myshopify.com/admin`
2. Go to **Settings** → **Apps and sales channels**
3. Click **"Develop apps"** → **"Create an app"**
4. Name it "Dropshipping Automation" (or any name)
5. Click **"Configure Admin API scopes"**
6. Select these scopes:
   - `read_products`
   - `write_products`
   - `read_orders`
   - `write_orders`
   - `read_fulfillments`
   - `write_fulfillments`
   - `read_customers`
7. Click **"Save"**
8. Click **"Install app"**
9. After installation, go to **"API credentials"** tab
10. Click **"Reveal token once"** next to Admin API access token
11. **Copy these values:**
    - `SHOPIFY_API_KEY` = App API key (shown in credentials)
    - `SHOPIFY_API_SECRET` = App API secret key (shown in credentials)
    - `SHOPIFY_STORE_NAME` = Your store name (e.g., "mystore" from mystore.myshopify.com)
    - `SHOPIFY_ACCESS_TOKEN` = Admin API access token (the one you revealed)

**Cost:** Free 3-day trial, then $29/month (or start with development store - free)

---

## 2. CJdropshipping Account ⭐ ESSENTIAL

**Website:** https://www.cjdropshipping.com

**Steps:**
1. Go to https://www.cjdropshipping.com
2. Click **"Sign Up"** (top right)
3. Register with email or Google account
4. Verify your email
5. Complete your profile

**Getting API Credentials:**
1. Log in to your account
2. Go to **"API Center"** or **"Developer"** section (usually in account settings)
3. Click **"Create API Key"** or **"Generate API"**
4. **Copy these values:**
    - `CJ_API_KEY` = Your API Key
    - `CJ_API_SECRET` = Your API Secret

**Alternative: AliExpress**
- If CJdropshipping doesn't work, you can use AliExpress
- Note: AliExpress API access may require business verification
- The system is configured for CJdropshipping primarily

**Cost:** Free account, pay only for products you fulfill

---

## 3. OpenAI Account ⭐ ESSENTIAL (For AI Features)

**Website:** https://platform.openai.com

**Steps:**
1. Go to https://platform.openai.com
2. Click **"Sign up"**
3. Create account with email or Google/Microsoft
4. Verify your email
5. Complete phone verification

**Getting API Key:**
1. Log in to https://platform.openai.com
2. Click your profile (top right) → **"View API keys"**
3. Click **"Create new secret key"**
4. Name it "Dropshipping System"
5. **Copy the key immediately** (you won't see it again!)
6. This is your `OPENAI_API_KEY`

**Cost:** 
- Pay-as-you-go (very affordable for this use case)
- ~$0.01-0.03 per product description
- ~$0.005 per customer message
- Start with $5-10 credit to test

---

## 4. TikTok Ads Account ⭐ RECOMMENDED

**Website:** https://ads.tiktok.com

**Steps:**
1. Go to https://ads.tiktok.com
2. Click **"Sign Up"** or **"Get Started"**
3. Choose **"Create an Advertiser Account"**
4. Fill in business information:
   - Business name
   - Industry
   - Country
5. Verify your email
6. Complete business verification (may require documents)

**Getting API Credentials:**
1. Log in to TikTok Ads Manager
2. Go to **"Tools"** → **"Marketing API"** (or Developer Center)
3. Click **"Create App"** or **"Register App"**
4. Fill in app details:
   - App Name: "Dropshipping Automation"
   - App Category: Marketing
   - Redirect URL: `http://localhost:8000` (for testing)
5. After app creation, note your:
   - `TIKTOK_CLIENT_ID` = App ID
   - `TIKTOK_CLIENT_SECRET` = App Secret
   - `TIKTOK_ADVERTISER_ID` = Your Advertiser ID (shown in Ads Manager dashboard)
6. Generate Access Token:
   - In Marketing API section, create access token
   - Grant permissions: Campaign Management, Ad Management
   - This is your `TIKTOK_ACCESS_TOKEN`

**Cost:** Pay only for ads you run (minimum $20 budget typically)

---

## 5. Facebook Ads Account ⭐ RECOMMENDED

**Website:** https://www.facebook.com/business

**Steps:**
1. Go to https://www.facebook.com/business
2. Click **"Create Account"**
3. Fill in business details:
   - Business name
   - Your name
   - Business email
4. Verify your email
5. Create Facebook Business Manager account
6. Verify your business (may require documents)

**Getting API Credentials:**
1. Go to https://developers.facebook.com
2. Click **"My Apps"** → **"Create App"**
3. Choose **"Business"** as app type
4. Fill in app details:
   - App Name: "Dropshipping Automation"
   - Business Account: Your business manager
5. Add **"Marketing API"** product to your app
6. Go to **"Settings"** → **"Basic"**
   - Note your `FACEBOOK_APP_ID` and `FACEBOOK_APP_SECRET`
7. Generate Access Token:
   - Go to **"Tools"** → **"Graph API Explorer"**
   - Select your app
   - Add permissions: `ads_read`, `ads_management`
   - Generate access token → This is your `FACEBOOK_ACCESS_TOKEN`
8. Get Ad Account ID:
   - Go to Business Manager → **"Ads Manager"**
   - Your Ad Account ID is shown (format: `act_123456789`)
   - This is your `FACEBOOK_AD_ACCOUNT_ID`

**Cost:** Pay only for ads you run (minimum $1 per day)

---

## 📝 Quick Setup Steps Summary

### Step 1: Create Accounts (30-60 minutes)
1. ✅ Sign up for Shopify → Get API credentials
2. ✅ Sign up for CJdropshipping → Get API key
3. ✅ Sign up for OpenAI → Get API key
4. ⭐ Sign up for TikTok Ads → Get API credentials
5. ⭐ Sign up for Facebook Ads → Get API credentials

### Step 2: Configure Your System (5 minutes)
1. Copy `.env.example` to `.env`
2. Fill in all the API keys you got above
3. Save the file

### Step 3: Test the System (5 minutes)
1. Start backend: `cd backend && python main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Visit http://localhost:3000
4. Check if everything works!

---

## 🎯 Minimum Setup (For Testing)

You can start with JUST these 3 accounts:

1. **Shopify** - To test store operations
2. **OpenAI** - To test AI features  
3. **CJdropshipping** - To test product sourcing

The system will work in **mock mode** for TikTok/Facebook ads until you add those credentials.

---

## 💡 Tips

1. **Start with Shopify Development Store** - Free, perfect for testing
2. **Use OpenAI credits** - Start with $5-10, very cheap for testing
3. **Test in mock mode first** - Don't need all accounts to start
4. **Read API documentation** - Each platform has guides for getting credentials
5. **Save all credentials** - Keep them in a secure password manager

---

## 🔐 Security Note

**NEVER commit your `.env` file to Git!**
- The `.env` file is in `.gitignore` for your protection
- Always keep API keys private
- Use environment variables in production

---

## ❓ Troubleshooting

### Can't find API settings?
- Each platform updates their UI frequently
- Search for "API", "Developer", "Integration" in their help docs
- Contact their support if needed

### API not working?
- Check if API key is correct (no extra spaces)
- Verify you have correct permissions/scopes
- Make sure account is verified (some require verification)

### Need help?
- See `docs/SETUP.md` for detailed instructions
- Check each platform's API documentation
- Review error messages in terminal logs

---

## ✅ Ready to Start?

Once you have your accounts set up:

1. ✅ Copy credentials to `config/.env`
2. ✅ Run the system (see QUICKSTART.md)
3. ✅ Start automating your business!

Good luck! 🚀

