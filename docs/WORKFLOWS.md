# Automation Workflows

This document describes the visual workflows for all automation processes in the system.

## 1. Product Discovery & Listing Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              PRODUCT DISCOVERY WORKFLOW                      │
└─────────────────────────────────────────────────────────────┘

    [Orchestrator] ──┐
    (Hourly Trigger) │
                     │
                     ▼
         ┌───────────────────────┐
         │ Product Discovery      │
         │ Service                │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Query CJdropshipping   │
         │ API for Trending       │
         │ Products               │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Filter by:             │
         │ • Profit Margin (30%+) │
         │ • Sales Volume          │
         │ • Price Range           │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Calculate Metrics:     │
         │ • Cost (price+shipping)│
         │ • Suggested Retail     │
         │ • Profit Margin        │
         │ • Expected Profit      │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Sort by Profitability │
         │ (Top 3-5 Products)     │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ For Each Product:     │
         │                       │
         │ 1. Generate AI        │
         │    Description         │
         │ 2. Generate SEO Title │
         │ 3. Generate Tags       │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Add to Shopify Store  │
         │ • Product Details     │
         │ • Images              │
         │ • Pricing             │
         │ • Inventory           │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Auto-Create Ad        │
         │ Campaign               │
         │ (TikTok/Facebook)     │
         └───────────────────────┘
```

## 2. Order Fulfillment Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              ORDER FULFILLMENT WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

    [Orchestrator] ──┐
    (Every 5 min)    │
                     │
                     ▼
         ┌───────────────────────┐
         │ Check Shopify for     │
         │ Pending Orders         │
         │ (Status: Unfulfilled) │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ For Each Order:       │
         │                       │
         │ • Extract Items       │
         │ • Get Shipping Address│
         │ • Get Customer Info   │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Create Fulfillment    │
         │ Request with CJ       │
         │                       │
         │ Payload:              │
         │ • SKU & Quantities    │
         │ • Shipping Address    │
         │ • Shipping Method    │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ CJ Processes Order    │
         │ • Validates Items     │
         │ • Processes Payment   │
         │ • Generates Tracking  │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Update Shopify Order  │
         │ • Fulfillment Status  │
         │ • Tracking Number    │
         │ • Tracking URL        │
         │ • Estimated Delivery  │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Customer Notification │
         │ (Auto-sent by Shopify)│
         │ • Order Shipped Email │
         │ • Tracking Info       │
         └───────────────────────┘
```

## 3. Ad Creation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              AD CREATION WORKFLOW                            │
└─────────────────────────────────────────────────────────────┘

    [New Product Added] ──┐
    OR                     │
    [Manual Trigger]       │
                           │
                           ▼
         ┌───────────────────────┐
         │ Get Product Info:     │
         │ • Title                │
         │ • Description          │
         │ • Images               │
         │ • Category             │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Generate Video Script │
         │ (AI Content Generator)│
         │                       │
         │ • Hook (0-3s)         │
         │ • Problem (3-6s)      │
         │ • Solution (6-12s)   │
         │ • CTA (12-15s)       │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Generate Ad Caption  │
         │ (AI Content Generator)│
         │                       │
         │ • Platform-specific   │
         │ • Hashtags            │
         │ • Call-to-Action      │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Generate Video        │
         │ (Video Generator)     │
         │                       │
         │ • Use Product Images  │
         │ • Add Text Overlays   │
         │ • Apply Transitions   │
         │ • Export Video        │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Upload Video to       │
         │ Cloud Storage         │
         │ (S3/Cloudinary)       │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Create Campaign       │
         │                       │
         │ Choose Platform:      │
         │ ┌─────────┬─────────┐│
         │ │ TikTok  │ Facebook ││
         │ └─────────┴─────────┘│
         └───────────┬────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
    ┌──────────┐          ┌──────────┐
    │ TikTok   │          │ Facebook │
    │ Campaign │          │ Campaign │
    └──────────┘          └──────────┘
         │                       │
         ▼                       ▼
    ┌──────────┐          ┌──────────┐
    │ Upload   │          │ Upload   │
    │ Video    │          │ Video    │
    └──────────┘          └──────────┘
         │                       │
         ▼                       ▼
    ┌──────────┐          ┌──────────┐
    │ Create   │          │ Create   │
    │ Ad Group │          │ Ad Set   │
    └──────────┘          └──────────┘
         │                       │
         ▼                       ▼
    ┌──────────┐          ┌──────────┐
    │ Set     │          │ Set      │
    │ Budget  │          │ Budget   │
    │ & Target│          │ & Target │
    └──────────┘          └──────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Activate Campaign     │
         │ • Set Status: Active  │
         │ • Start Date: Now     │
         └───────────────────────┘
```

## 4. Customer Service Workflow

```
┌─────────────────────────────────────────────────────────────┐
│           CUSTOMER SERVICE WORKFLOW                          │
└─────────────────────────────────────────────────────────────┘

    [Orchestrator] ──┐
    (Every 3 min)    │
                     │
                     ▼
         ┌───────────────────────┐
         │ Check for New        │
         │ Customer Messages    │
         │                       │
         │ Sources:             │
         │ • Shopify Chat       │
         │ • Email              │
         │ • Support Tickets    │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Filter Unanswered    │
         │ Messages              │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ For Each Message:    │
         │                       │
         │ • Extract Content    │
         │ • Check for Order ID │
         │ • Get Customer Info  │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Get Order Context     │
         │ (if order_id exists)  │
         │                       │
         │ • Order Status        │
         │ • Tracking Info       │
         │ • Product Details    │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Generate AI Response  │
         │                       │
         │ Prompt Includes:      │
         │ • Customer Message    │
         │ • Order Context       │
         │ • Store Policies      │
         │                       │
         │ AI Considers:         │
         │ • Message Type        │
         │ • Urgency             │
         │ • Appropriate Tone    │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Validate Response     │
         │ • Appropriate?       │
         │ • Complete?          │
         │ • Helpful?           │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Send Response         │
         │ • Via Original Channel│
         │ • Email/Chat/Ticket   │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Mark Message as       │
         │ Answered              │
         │ • Update Status       │
         │ • Log Response        │
         └───────────────────────┘
```

## 5. Analytics & Reporting Workflow

```
┌─────────────────────────────────────────────────────────────┐
│           ANALYTICS & REPORTING WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

    [Dashboard Request] ──┐
    OR                     │
    [Scheduled Report]     │
                           │
                           ▼
         ┌───────────────────────┐
         │ Analytics Service     │
         │ Triggered             │
         └───────────┬────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
    ┌──────────┐          ┌──────────┐
    │ Get      │          │ Get      │
    │ Sales    │          │ Ad Spend │
    │ Data     │          │ Data     │
    └──────────┘          └──────────┘
         │                       │
         ▼                       ▼
    ┌──────────┐          ┌──────────┐
    │ Query    │          │ Query    │
    │ Shopify  │          │ TikTok   │
    │ Orders   │          │ Facebook │
    └──────────┘          └──────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Calculate Metrics:   │
         │                       │
         │ • Total Sales        │
         │ • Total Profit       │
         │ • Total Orders       │
         │ • Total Ad Spend     │
         │ • ROI                │
         │ • Conversion Rate    │
         │ • Avg Order Value    │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Get Time-Series Data: │
         │                       │
         │ • Sales by Date       │
         │ • Profit by Date      │
         │ • Orders by Date      │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Get Top Products      │
         │ • Revenue             │
         │ • Quantity Sold      │
         │ • Profit              │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Get Ad Performance    │
         │ • Platform            │
         │ • Spend               │
         │ • Impressions         │
         │ • Clicks              │
         │ • Conversions         │
         │ • ROAS                │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Aggregate Data        │
         │ into DashboardMetrics │
         └───────────┬────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Return to Frontend    │
         │ (Dashboard Display)  │
         └───────────────────────┘
```

## 6. Complete System Automation Loop

```
┌─────────────────────────────────────────────────────────────┐
│           COMPLETE SYSTEM AUTOMATION                          │
└─────────────────────────────────────────────────────────────┘

         ┌───────────────────────┐
         │ Automation Orchestrator│
         │ Started                │
         └───────────┬────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
    ┌──────────┐          ┌──────────┐
    │ Product  │          │ Order    │
    │ Discovery│          │ Fulfill  │
    │ Loop     │          │ Loop     │
    │ (Hourly) │          │ (5 min)  │
    └──────────┘          └──────────┘
         │                       │
         ▼                       ▼
    ┌──────────┐          ┌──────────┐
    │ Customer │          │ Ad      │
    │ Service  │          │ Optimize│
    │ Loop     │          │ Loop    │
    │ (3 min)  │          │ (6 hrs) │
    └──────────┘          └──────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ All Loops Running     │
         │ Concurrently          │
         │                       │
         │ • Error Handling      │
         │ • Logging             │
         │ • Recovery            │
         └───────────────────────┘
```

## Workflow Notes

1. **All workflows run continuously** once the orchestrator is started
2. **Intervals are configurable** via settings
3. **Error handling** ensures workflows continue even if individual operations fail
4. **Logging** tracks all operations for monitoring and debugging
5. **Manual triggers** available via API endpoints for immediate execution

