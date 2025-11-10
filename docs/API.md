# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API uses API key authentication via environment variables. In production, implement proper authentication mechanisms.

## Endpoints

### Product Discovery

#### Discover Products
```http
GET /products/discover
```

**Query Parameters:**
- `category` (optional): Product category filter
- `min_margin` (optional): Minimum profit margin (0.0-1.0)
- `limit` (optional): Maximum number of products (default: 20)

**Response:**
```json
[
  {
    "id": "product-001",
    "title": "Wireless Bluetooth Earbuds",
    "description": "Premium wireless earbuds...",
    "price": 45.00,
    "cost": 15.00,
    "margin": 0.667,
    "profit": 30.00,
    "currency": "USD",
    "category": "Electronics",
    "images": ["https://..."],
    "supplier_id": "supplier-1",
    "supplier_name": "CJ Supplier",
    "supplier_url": "https://...",
    "shipping_info": {
      "cost": 3.50,
      "time": "7-15 days"
    },
    "status": "discovered",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Store Management

#### Create Store
```http
POST /store/create
```

**Request Body:**
```json
{
  "store_name": "mystore",
  "store_url": "https://mystore.myshopify.com",
  "theme": "modern",
  "brand_name": "My Brand",
  "brand_description": "Premium products",
  "logo_url": "https://...",
  "primary_color": "#000000",
  "secondary_color": "#ffffff",
  "payment_methods": ["credit_card", "paypal"],
  "shipping_zones": []
}
```

#### Add Product
```http
POST /products/add
```

**Request Body:** (Product object as shown above)

### Ad Management

#### Create Ad Campaign
```http
POST /ads/create
```

**Request Body:**
```json
{
  "name": "Promote Product X",
  "platform": "tiktok",
  "product_id": "product-001",
  "budget": 50.0,
  "daily_budget": 10.0,
  "target_audience": {
    "age_range": [18, 45],
    "genders": [1, 2],
    "location": ["US"]
  },
  "creative_caption": "Check out this amazing product!",
  "status": "draft"
}
```

#### List Campaigns
```http
GET /ads/campaigns
```

### Order Management

#### Get Pending Orders
```http
GET /orders/pending
```

**Response:**
```json
[
  {
    "id": "order-001",
    "order_number": "#1001",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "items": [
      {
        "title": "Product 1",
        "quantity": 2,
        "price": 29.99,
        "sku": "SKU-001"
      }
    ],
    "total": 59.98,
    "currency": "USD",
    "shipping_address": {
      "name": "John Doe",
      "address1": "123 Main St",
      "city": "New York",
      "province": "NY",
      "zip": "10001",
      "country": "US"
    },
    "status": "paid",
    "fulfillment_status": "unfulfilled",
    "tracking_number": null,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Fulfill Order
```http
POST /orders/{order_id}/fulfill
```

### Customer Service

#### Get Messages
```http
GET /customer/messages
```

**Query Parameters:**
- `answered` (optional): Filter by answered status (default: false)

#### Respond to Message
```http
POST /customer/messages/{message_id}/respond
```

### Analytics

#### Get Dashboard Metrics
```http
GET /dashboard/metrics
```

**Query Parameters:**
- `start_date` (optional): Start date (ISO format)
- `end_date` (optional): End date (ISO format)

**Response:**
```json
{
  "total_sales": 5000.0,
  "total_profit": 2500.0,
  "total_orders": 125,
  "total_ad_spend": 350.0,
  "roi": 614.29,
  "conversion_rate": 2.5,
  "average_order_value": 40.0,
  "top_products": [
    {
      "name": "Product 1",
      "sales": 1200.0,
      "revenue": 1200.0,
      "quantity": 30
    }
  ],
  "sales_by_date": [
    {
      "date": "2024-01-01",
      "sales": 150.0
    }
  ],
  "profit_by_date": [
    {
      "date": "2024-01-01",
      "profit": 105.0
    }
  ],
  "ad_performance": [
    {
      "platform": "TikTok",
      "spend": 150.0,
      "impressions": 50000,
      "clicks": 2500,
      "conversions": 62,
      "roas": 3.5
    }
  ]
}
```

### Automation Control

#### Start Automation
```http
POST /automation/start
```

#### Stop Automation
```http
POST /automation/stop
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

API rate limits are not currently implemented but should be added in production to prevent abuse.

## Interactive API Docs

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

