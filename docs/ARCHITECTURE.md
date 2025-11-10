# System Architecture

## Overview

The Automated Dropshipping System is a comprehensive platform that automates all aspects of a dropshipping business. The system is built with a microservices-inspired architecture using FastAPI for the backend and React for the frontend.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     React Dashboard (Frontend)               │
│                     http://localhost:3000                    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST API
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              FastAPI Backend (Main Service)                 │
│              http://localhost:8000                           │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Automation Orchestrator                        │ │
│  │  • Product Discovery Loop                               │ │
│  │  • Order Fulfillment Loop                               │ │
│  │  • Customer Service Loop                                │ │
│  │  • Ad Optimization Loop                                 │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────┬───────────────┬───────────────┬───────────────┘
             │               │               │
    ┌────────▼──────┐ ┌──────▼──────┐ ┌─────▼─────┐
    │   Services    │ │  Integrations│ │   Agents  │
    │               │ │              │ │           │
    │ • Product     │ │ • Shopify    │ │ • AI CS   │
    │   Discovery   │ │ • CJdropship │ │   Agent   │
    │ • Analytics   │ │ • TikTok Ads │ │           │
    │ • Fulfillment │ │ • Facebook   │ │           │
    └───────────────┘ │   Ads        │ └───────────┘
                     └──────────────┘
```

## Core Components

### 1. Frontend (React Dashboard)
- **Location**: `frontend/`
- **Technology**: React, Vite, Recharts
- **Purpose**: User interface for monitoring and controlling the system
- **Pages**:
  - Dashboard: Analytics and metrics
  - Products: Product discovery and management
  - Orders: Order management and fulfillment
  - Ads: Ad campaign management
  - Customer Service: Message handling

### 2. Backend API (FastAPI)
- **Location**: `backend/`
- **Technology**: FastAPI, Python
- **Purpose**: REST API for all operations
- **Endpoints**: See API documentation

### 3. Core Services

#### Product Discovery Service
- **File**: `backend/services/product_discovery.py`
- **Purpose**: Find trending and high-margin products
- **Integrations**: CJdropshipping API, AliExpress (via CJ)
- **Features**:
  - Margin calculation
  - Sales volume filtering
  - Trending product detection

#### Shopify Manager
- **File**: `backend/services/shopify_manager.py`
- **Purpose**: Manage Shopify store operations
- **Features**:
  - Product listing
  - Store configuration
  - Order management
  - Inventory updates

#### Ad Manager
- **File**: `backend/services/ad_manager.py`
- **Purpose**: Create and manage ad campaigns
- **Integrations**: TikTok Ads API, Facebook Ads API
- **Features**:
  - Campaign creation
  - Video ad generation
  - Caption generation
  - Performance tracking

#### Order Fulfillment Service
- **File**: `backend/services/order_fulfillment.py`
- **Purpose**: Automatically fulfill orders
- **Features**:
  - Auto-fulfillment
  - Tracking updates
  - Supplier integration

#### Customer Service Agent
- **File**: `backend/services/customer_service_agent.py`
- **Purpose**: AI-powered customer support
- **Features**:
  - Message handling
  - AI response generation
  - Order context awareness

#### Analytics Service
- **File**: `backend/services/analytics.py`
- **Purpose**: Calculate metrics and analytics
- **Features**:
  - Sales tracking
  - Profit calculation
  - ROI analysis
  - Performance metrics

### 4. AI Services

#### AI Content Generator
- **File**: `backend/services/ai_content_generator.py`
- **Purpose**: Generate content using AI
- **Features**:
  - Product descriptions
  - SEO titles
  - Ad captions
  - Video scripts

#### Video Generator
- **File**: `backend/services/video_generator.py`
- **Purpose**: Generate product ad videos
- **Features**:
  - Image-based videos
  - Text overlays
  - Script-based generation

### 5. Automation Orchestrator
- **File**: `backend/services/orchestrator.py`
- **Purpose**: Coordinate all automation workflows
- **Features**:
  - Continuous loops for each automation
  - Error handling and recovery
  - Configurable intervals

## Data Flow

### Product Discovery Flow
1. Orchestrator triggers product discovery (hourly)
2. Product Discovery Service queries CJdropshipping API
3. Products filtered by margin and sales volume
4. Top products added to Shopify store
5. Ad campaigns auto-created for new products

### Order Fulfillment Flow
1. New order created in Shopify
2. Orchestrator detects pending order (every 5 minutes)
3. Order Fulfillment Service creates fulfillment request with CJ
4. Tracking number received and updated in Shopify
5. Customer receives tracking notification

### Customer Service Flow
1. Customer message received (Shopify/Email)
2. Orchestrator detects new message (every 3 minutes)
3. Customer Service Agent generates AI response
4. Response sent automatically
5. Message marked as answered

### Ad Creation Flow
1. New product added to store
2. Orchestrator triggers ad creation
3. AI generates video script and caption
4. Video generated from product images
5. Ad campaign created on TikTok/Facebook
6. Campaign goes live automatically

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.10+
- **API Client**: httpx, requests
- **AI**: OpenAI API, Anthropic API
- **Video**: MoviePy
- **Task Queue**: Celery (optional)
- **Database**: PostgreSQL (optional)

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Routing**: React Router

### External APIs
- Shopify Admin API
- CJdropshipping API
- TikTok Business API
- Facebook Marketing API
- OpenAI API

## Security Considerations

1. **API Keys**: Stored in environment variables, never committed
2. **CORS**: Configured for specific origins
3. **Rate Limiting**: Implemented to prevent API abuse
4. **Error Handling**: Sensitive information not exposed in errors
5. **Authentication**: API key authentication for external APIs

## Scalability

The system is designed to scale:
- Stateless API design allows horizontal scaling
- Celery for async task processing (optional)
- Database connection pooling
- Caching strategies for frequently accessed data
- Rate limiting to respect API quotas

## Monitoring & Logging

- Structured logging with Python logging
- Error tracking and reporting
- Performance metrics
- API usage monitoring
- Dashboard metrics tracking

