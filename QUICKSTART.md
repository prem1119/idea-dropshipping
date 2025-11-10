# Quick Start Guide

Get your fully automated dropshipping system running in minutes!

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] API keys ready (see below)

## Step 1: Install Dependencies

### Backend
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Step 2: Configure API Keys

Copy the example environment file:
```bash
cp config/.env.example config/.env
```

Edit `config/.env` and add your API keys. **Minimum required:**
- Shopify credentials (for store operations)
- At least one: CJdropshipping API key OR use mock mode for testing
- OpenAI API key (for AI features)

**Note:** The system works in mock mode without all APIs configured, perfect for testing!

## Step 3: Start the System

### Terminal 1 - Backend
```bash
# From project root
cd backend
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Frontend
```bash
# From frontend directory
npm run dev
```

You should see:
```
VITE ready in XXX ms
➜  Local:   http://localhost:3000/
```

## Step 4: Access the Dashboard

Open your browser to: **http://localhost:3000**

You should see the dashboard with:
- Metrics overview
- Product discovery
- Orders management
- Ad campaigns
- Customer service

## Step 5: Start Automation

Once everything is running:

1. **Discover Products**: Go to Products page and browse trending products
2. **Add Products**: Click "Add to Store" on products you want to sell
3. **View Orders**: Check Orders page for pending fulfillments
4. **Monitor Metrics**: Dashboard shows real-time sales and profit

## Testing Without API Keys

The system includes mock modes that work without API keys:

- **Product Discovery**: Returns mock trending products
- **Order Fulfillment**: Simulates fulfillment process
- **Customer Service**: Uses mock responses
- **Analytics**: Shows sample metrics

This lets you test the entire system before setting up real API integrations!

## Next Steps

1. **Set up Shopify store**: Create a development store and get API credentials
2. **Get CJdropshipping account**: Sign up at cjdropshipping.com for product fulfillment
3. **Configure ads**: Set up TikTok/Facebook ad accounts for automated campaigns
4. **Enable OpenAI**: Add API key for AI-powered content generation

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.10+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is available

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Delete `node_modules` and run `npm install` again
- Check port 3000 is available

### API errors
- Check `.env` file exists in `config/` directory
- Verify API keys are correct
- Review error messages in terminal/logs

## Getting Help

- **Setup Issues**: See `docs/SETUP.md`
- **Architecture**: See `docs/ARCHITECTURE.md`
- **Workflows**: See `docs/WORKFLOWS.md`
- **API Docs**: See `docs/API.md` or visit http://localhost:8000/docs

## Production Deployment

For production:
1. Set `DEBUG=False` in `.env`
2. Use PostgreSQL database
3. Set up Redis for Celery tasks
4. Configure proper CORS origins
5. Set up SSL/TLS
6. Use environment variables for secrets
7. Set up monitoring and logging

Enjoy your fully automated dropshipping system! 🚀

