# Fully Automated Dropshipping Business System

A comprehensive, hands-free dropshipping automation platform that handles everything from product discovery to customer service.

## 🚀 Features

- **Product Discovery**: Automatically finds trending and high-margin products from AliExpress/CJdropshipping
- **Shopify Automation**: Auto-builds stores with branding, descriptions, and product images
- **Ad Creation**: Automatically generates and manages TikTok/Facebook ads with AI-generated videos and captions
- **Order Fulfillment**: Automatically fulfills orders and updates tracking information
- **AI Customer Service**: Handles all customer service messages autonomously
- **Analytics Dashboard**: Real-time metrics for sales, profit, ad spend, and performance

## 📁 Project Structure

```
├── backend/              # FastAPI backend services
│   ├── api/             # API routes
│   ├── services/        # Business logic
│   ├── agents/          # AI agents
│   ├── integrations/    # External API integrations
│   └── models/          # Data models
├── frontend/            # React dashboard
├── automation/           # Automation workflows
├── config/              # Configuration files
└── docs/                # Documentation

```

## 🛠️ Setup

See [SETUP.md](docs/SETUP.md) for detailed installation instructions.

## 📊 Dashboard

Access the dashboard at `http://localhost:3000` after starting the services.

## 🔧 Configuration

1. Copy `config/.env.example` to `config/.env`
2. Fill in your API keys for:
   - Shopify
   - AliExpress/CJdropshipping
   - TikTok Ads API (optional)
   - Facebook Ads API (optional)
   - **Hugging Face** (for AI features) OR OpenAI (alternative)

**Note:** The system now supports **Hugging Face** as a free alternative to OpenAI for AI features!

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** ⭐ **START HERE** - Websites to sign up for and API keys guide
- **[ACCOUNTS_CHECKLIST.md](ACCOUNTS_CHECKLIST.md)** - Track your account setup progress
- [Quick Start Guide](QUICKSTART.md) - Get started in minutes!
- [Setup Instructions](docs/SETUP.md) - Detailed setup guide
- [Architecture Overview](docs/ARCHITECTURE.md) - System architecture
- [Workflow Diagrams](docs/WORKFLOWS.md) - Visual workflow documentation
- [Visual Workflow Summary](docs/VISUAL_WORKFLOW_SUMMARY.md) - Quick reference
- [API Documentation](docs/API.md) - API endpoints reference

## 🎯 Key Features

### ✅ Product Discovery
- Automatic trending product detection
- High-margin filtering (30%+ profit margin)
- Integration with CJdropshipping and AliExpress
- Sales volume analysis

### ✅ Shopify Automation
- Auto-build store with branding
- AI-generated product descriptions
- SEO-optimized titles and tags
- Automatic product listing

### ✅ Ad Creation
- Auto-generate TikTok and Facebook ads
- AI-powered video scripts
- AI-generated captions
- Automatic campaign creation and management

### ✅ Order Fulfillment
- Automatic order processing
- Real-time tracking updates
- Customer notifications
- Full order lifecycle management

### ✅ AI Customer Service
- Automatic message handling
- Context-aware responses
- Order information integration
- 24/7 automated support

### ✅ Analytics Dashboard
- Real-time sales metrics
- Profit tracking
- ROI analysis
- Ad performance monitoring
- Top products tracking

## 🔄 Automation Loops

The system runs 4 continuous automation loops:

1. **Product Discovery** (Hourly) - Finds and adds trending products
2. **Order Fulfillment** (Every 5 min) - Processes pending orders
3. **Customer Service** (Every 3 min) - Handles customer messages
4. **Ad Optimization** (Every 6 hours) - Optimizes ad campaigns

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
cd frontend && npm install

# 2. Configure API keys
cp config/.env.example config/.env
# Edit config/.env with your API keys

# 3. Start backend
cd backend && python main.py

# 4. Start frontend (new terminal)
cd frontend && npm run dev

# 5. Access dashboard
# Open http://localhost:3000
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions!

