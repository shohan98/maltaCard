# 🚀 MaltaCard API - Ultimate Integration Guide

Welcome to the MaltaCard API! This comprehensive guide will help you integrate with our card management system quickly and efficiently.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Request/Response Examples](#requestresponse-examples)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [SDK Examples](#sdk-examples)
8. [Testing](#testing)
9. [Production Deployment](#production-deployment)
10. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Base URL
```
Development: http://localhost:8000/api/
Production: https://your-domain.com/api/
```

### Authentication
All API endpoints require authentication using Bearer tokens.

```bash
# Get your API token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password"
  }'
```

### First API Call
```bash
# List all card types
curl -X GET http://localhost:8000/api/cards/card-types/ \
  -H "Authorization: Token your-token-here"
```

---

## 🔐 Authentication

### Authentication Methods

#### 1. Token Authentication (Recommended)
```bash
Authorization: Token your-token-here
```

#### 2. Bearer Token
```bash
Authorization: Bearer your-token-here
```

### Getting Your Token

#### Step 1: Register/Login
```bash
# Register a new account
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@example.com",
    "password": "secure-password123",
    "password_confirm": "secure-password123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login to get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@example.com",
    "password": "secure-password123"
  }'
```

#### Step 2: Use the Token
```json
{
  "token": "your-auth-token-here",
  "user": {
    "id": 1,
    "email": "developer@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Token Management

#### Refresh Token
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Authorization: Token your-token-here"
```

#### Logout
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token your-token-here"
```

---

## 📡 API Endpoints

### 🔐 Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | Register new user |
| `POST` | `/api/auth/login/` | Login and get token |
| `POST` | `/api/auth/logout/` | Logout and invalidate token |
| `GET` | `/api/auth/me/` | Get current user info |
| `GET` | `/api/auth/refresh/` | Refresh authentication token |

### 🃏 Card Types Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cards/card-types/` | List all card types |
| `POST` | `/api/cards/card-types/` | Create new card type |
| `GET` | `/api/cards/card-types/{id}/` | Get specific card type |
| `PUT` | `/api/cards/card-types/{id}/` | Update card type |
| `DELETE` | `/api/cards/card-types/{id}/` | Delete card type |
| `GET` | `/api/cards/card-types/popular/` | Get popular card types |
| `GET` | `/api/cards/card-types/by_duration/` | Filter by duration |
| `GET` | `/api/cards/card-types/price_range/` | Filter by price range |
| `POST` | `/api/cards/card-types/{id}/toggle_popular/` | Toggle popular status |

### 🎴 Cards Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cards/cards/` | List all cards |
| `POST` | `/api/cards/cards/` | Create new card |
| `GET` | `/api/cards/cards/{id}/` | Get specific card |
| `PUT` | `/api/cards/cards/{id}/` | Update card |
| `DELETE` | `/api/cards/cards/{id}/` | Delete card |
| `GET` | `/api/cards/cards/virtual_cards/` | Get virtual cards only |
| `GET` | `/api/cards/cards/physical_cards/` | Get physical cards only |
| `GET` | `/api/cards/cards/by_type/` | Filter by card type |
| `GET` | `/api/cards/cards/by_price_range/` | Filter by price range |

### 📦 Card Orders Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cards/orders/` | List all orders |
| `POST` | `/api/cards/orders/` | Create new order |
| `GET` | `/api/cards/orders/{id}/` | Get specific order |
| `PUT` | `/api/cards/orders/{id}/` | Update order |
| `DELETE` | `/api/cards/orders/{id}/` | Delete order |
| `GET` | `/api/cards/orders/my_orders/` | Get user's orders |
| `GET` | `/api/cards/orders/pending_orders/` | Get pending orders |
| `POST` | `/api/cards/orders/{id}/cancel_order/` | Cancel order |
| `POST` | `/api/cards/orders/{id}/update_status/` | Update order status |

### 👥 User Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/auth/users/` | List all users (admin only) |
| `GET` | `/api/auth/users/{id}/` | Get specific user |
| `PUT` | `/api/auth/users/{id}/` | Update user |
| `DELETE` | `/api/auth/users/{id}/` | Delete user |
| `GET` | `/api/auth/users/me/` | Get current user profile |

---

## 📝 Request/Response Examples

### 🔐 Authentication Examples

#### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_joined": "2024-01-15T10:30:00Z"
    },
    "token": "your-auth-token-here"
  }
}
```

#### Login User
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "your-auth-token-here",
    "user": {
      "id": 1,
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe"
    }
  }
}
```

### 🃏 Card Types Examples

#### List Card Types
```bash
curl -X GET http://localhost:8000/api/cards/card-types/ \
  -H "Authorization: Token your-token-here"
```

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Premium Virtual Card",
      "description": "High-limit virtual card for online transactions",
      "duration_type": "monthly",
      "duration_type_display": "Monthly",
      "price": "29.99",
      "features": ["Unlimited transactions", "24/7 support"],
      "max_transactions": 1000,
      "daily_limit": "5000.00",
      "monthly_limit": "50000.00",
      "is_popular": true,
      "sort_order": 1,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "is_active": true
    }
  ]
}
```

#### Create Card Type
```bash
curl -X POST http://localhost:8000/api/cards/card-types/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Basic Virtual Card",
    "description": "Entry-level virtual card",
    "duration_type": "monthly",
    "price": "9.99",
    "features": ["Basic transactions", "Email support"],
    "max_transactions": 100,
    "daily_limit": "1000.00",
    "monthly_limit": "10000.00",
    "is_popular": false,
    "sort_order": 2
  }'
```

#### Get Popular Card Types
```bash
curl -X GET http://localhost:8000/api/cards/card-types/popular/ \
  -H "Authorization: Token your-token-here"
```

### 🎴 Cards Examples

#### List Cards
```bash
curl -X GET http://localhost:8000/api/cards/cards/ \
  -H "Authorization: Token your-token-here"
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Premium Virtual Card",
      "card_type": 1,
      "card_type_display": "Premium Virtual Card",
      "description": "High-limit virtual card",
      "price": "29.99",
      "total_orders": 150,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "is_active": true
    }
  ]
}
```

#### Get Virtual Cards Only
```bash
curl -X GET http://localhost:8000/api/cards/cards/virtual_cards/ \
  -H "Authorization: Token your-token-here"
```

#### Filter Cards by Price Range
```bash
curl -X GET "http://localhost:8000/api/cards/cards/by_price_range/?min_price=10&max_price=50" \
  -H "Authorization: Token your-token-here"
```

### 📦 Card Orders Examples

#### Create Order
```bash
curl -X POST http://localhost:8000/api/cards/orders/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": 1,
    "quantity": 2,
    "shipping_address": "123 Main St, City, State 12345",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "USA",
    "phone_number": "+1234567890"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Order created successfully",
  "data": {
    "id": "uuid-here",
    "user": {
      "id": 1,
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "card": {
      "id": 1,
      "name": "Premium Virtual Card",
      "price": "29.99"
    },
    "quantity": 2,
    "status": "pending",
    "status_display": "Pending",
    "total_amount": "59.98",
    "shipping_address": "123 Main St, City, State 12345",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "USA",
    "phone_number": "+1234567890",
    "order_date": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "is_active": true
  }
}
```

#### Get User's Orders
```bash
curl -X GET http://localhost:8000/api/cards/orders/my_orders/ \
  -H "Authorization: Token your-token-here"
```

#### Cancel Order
```bash
curl -X POST http://localhost:8000/api/cards/orders/1/cancel_order/ \
  -H "Authorization: Token your-token-here"
```

#### Update Order Status
```bash
curl -X POST http://localhost:8000/api/cards/orders/1/update_status/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "processing"
  }'
```

---

## 🔍 Query Parameters & Filtering

### Pagination
```bash
# Get first page (default 10 items)
GET /api/cards/card-types/?page=1

# Get specific page
GET /api/cards/card-types/?page=2

# Custom page size
GET /api/cards/card-types/?page_size=20
```

### Search
```bash
# Search by name
GET /api/cards/card-types/?search=premium

# Search in multiple fields
GET /api/cards/cards/?search=virtual
```

### Filtering
```bash
# Filter by price range
GET /api/cards/card-types/?price_min=10&price_max=50

# Filter by duration
GET /api/cards/card-types/?duration_type=monthly

# Filter by popularity
GET /api/cards/card-types/?is_popular=true

# Filter by status
GET /api/cards/orders/?status=pending

# Filter by date range
GET /api/cards/orders/?order_date_after=2024-01-01&order_date_before=2024-01-31
```

### Sorting
```bash
# Sort by price (ascending)
GET /api/cards/card-types/?ordering=price

# Sort by price (descending)
GET /api/cards/card-types/?ordering=-price

# Sort by multiple fields
GET /api/cards/card-types/?ordering=sort_order,name
```

---

## ❌ Error Handling

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `201` | Created | Resource created successfully |
| `400` | Bad Request | Invalid request data |
| `401` | Unauthorized | Authentication required |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource not found |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Server error |

### Error Response Format
```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field_name": ["Specific error message"]
  },
  "status_code": 400
}
```

### Common Error Examples

#### Authentication Error
```json
{
  "success": false,
  "message": "Authentication credentials were not provided",
  "status_code": 401
}
```

#### Validation Error
```json
{
  "success": false,
  "message": "Invalid data provided",
  "errors": {
    "email": ["This field is required."],
    "password": ["This password is too short."]
  },
  "status_code": 400
}
```

#### Not Found Error
```json
{
  "success": false,
  "message": "Card type not found",
  "status_code": 404
}
```

---

## ⚡ Rate Limiting

### Rate Limits
- **API endpoints**: 10 requests per second
- **Authentication endpoints**: 5 requests per minute
- **Admin endpoints**: 2 requests per second

### Rate Limit Headers
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 8
X-RateLimit-Reset: 1642234567
```

### Rate Limit Exceeded Response
```json
{
  "success": false,
  "message": "Rate limit exceeded. Please try again later.",
  "status_code": 429
}
```

---

## 🛠️ SDK Examples

### JavaScript/Node.js

#### Using Axios
```javascript
const axios = require('axios');

class MaltaCardAPI {
  constructor(baseURL, token) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    });
  }

  // Get all card types
  async getCardTypes(params = {}) {
    const response = await this.client.get('/api/cards/card-types/', { params });
    return response.data;
  }

  // Create new order
  async createOrder(orderData) {
    const response = await this.client.post('/api/cards/orders/', orderData);
    return response.data;
  }

  // Get user's orders
  async getMyOrders() {
    const response = await this.client.get('/api/cards/orders/my_orders/');
    return response.data;
  }
}

// Usage
const api = new MaltaCardAPI('http://localhost:8000', 'your-token');
const cardTypes = await api.getCardTypes();
```

#### Using Fetch
```javascript
class MaltaCardAPI {
  constructor(baseURL, token) {
    this.baseURL = baseURL;
    this.token = token;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Authorization': `Token ${this.token}`,
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };

    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'API request failed');
    }

    return data;
  }

  async getCardTypes() {
    return this.request('/api/cards/card-types/');
  }

  async createOrder(orderData) {
    return this.request('/api/cards/orders/', {
      method: 'POST',
      body: JSON.stringify(orderData)
    });
  }
}
```

### Python

#### Using Requests
```python
import requests

class MaltaCardAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }

    def get_card_types(self, params=None):
        response = requests.get(
            f'{self.base_url}/api/cards/card-types/',
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def create_order(self, order_data):
        response = requests.post(
            f'{self.base_url}/api/cards/orders/',
            headers=self.headers,
            json=order_data
        )
        response.raise_for_status()
        return response.json()

    def get_my_orders(self):
        response = requests.get(
            f'{self.base_url}/api/cards/orders/my_orders/',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Usage
api = MaltaCardAPI('http://localhost:8000', 'your-token')
card_types = api.get_card_types()
```

### PHP

```php
class MaltaCardAPI {
    private $baseUrl;
    private $token;

    public function __construct($baseUrl, $token) {
        $this->baseUrl = $baseUrl;
        $this->token = $token;
    }

    private function request($endpoint, $method = 'GET', $data = null) {
        $url = $this->baseUrl . $endpoint;
        
        $headers = [
            'Authorization: Token ' . $this->token,
            'Content-Type: application/json'
        ];

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

        if ($data) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpCode >= 400) {
            throw new Exception('API request failed: ' . $response);
        }

        return json_decode($response, true);
    }

    public function getCardTypes($params = []) {
        $query = http_build_query($params);
        return $this->request('/api/cards/card-types/?' . $query);
    }

    public function createOrder($orderData) {
        return $this->request('/api/cards/orders/', 'POST', $orderData);
    }
}

// Usage
$api = new MaltaCardAPI('http://localhost:8000', 'your-token');
$cardTypes = $api->getCardTypes();
```

---

## 🧪 Testing

### Testing Environment
```bash
# Development server
http://localhost:8000/api/

# Swagger documentation
http://localhost:8000/swagger/
```

### Testing with cURL

#### Test Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### Test Card Types
```bash
# Get all card types
curl -X GET http://localhost:8000/api/cards/card-types/ \
  -H "Authorization: Token your-token"

# Create card type
curl -X POST http://localhost:8000/api/cards/card-types/ \
  -H "Authorization: Token your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Card",
    "description": "Test description",
    "duration_type": "monthly",
    "price": "19.99",
    "features": ["Feature 1", "Feature 2"],
    "max_transactions": 500,
    "daily_limit": "2000.00",
    "monthly_limit": "20000.00"
  }'
```

#### Test Orders
```bash
# Create order
curl -X POST http://localhost:8000/api/cards/orders/ \
  -H "Authorization: Token your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": 1,
    "quantity": 1,
    "shipping_address": "123 Test St",
    "city": "Test City",
    "state": "TS",
    "postal_code": "12345",
    "country": "Test Country",
    "phone_number": "+1234567890"
  }'

# Get my orders
curl -X GET http://localhost:8000/api/cards/orders/my_orders/ \
  -H "Authorization: Token your-token"
```

### Testing with Postman

1. **Import Collection**
   - Download the Postman collection from `/api/swagger/`
   - Import into Postman

2. **Set Environment Variables**
   ```
   base_url: http://localhost:8000
   token: your-auth-token
   ```

3. **Test Flow**
   - Register/Login to get token
   - Set token in environment
   - Test all endpoints

---

## 🚀 Production Deployment

### Environment Setup
```bash
# Production environment variables
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@host:port/db
REDIS_URL=redis://redis-host:6379/0
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Docker Deployment
```bash
# Build and start services
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### SSL/HTTPS Setup
```nginx
# nginx.conf SSL configuration
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # ... rest of configuration
}
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Authentication Errors
**Problem**: `401 Unauthorized`
```json
{
  "success": false,
  "message": "Authentication credentials were not provided"
}
```

**Solution**:
- Check if token is included in headers
- Verify token is valid and not expired
- Re-login to get new token

#### 2. CSRF Errors
**Problem**: `403 Forbidden - CSRF Failed`
```json
{
  "success": false,
  "message": "CSRF Failed: CSRF token missing"
}
```

**Solution**:
- API endpoints don't require CSRF tokens
- Use token authentication instead of session
- Check if using correct authentication method

#### 3. Rate Limiting
**Problem**: `429 Too Many Requests`
```json
{
  "success": false,
  "message": "Rate limit exceeded"
}
```

**Solution**:
- Implement exponential backoff
- Reduce request frequency
- Contact support for higher limits

#### 4. Database Connection
**Problem**: `500 Internal Server Error`
```json
{
  "success": false,
  "message": "Database connection failed"
}
```

**Solution**:
- Check database service is running
- Verify database credentials
- Check network connectivity

### Debug Mode
```bash
# Enable debug mode for development
DEBUG=True

# Check logs
docker-compose logs web
docker-compose logs db
```

### Health Check
```bash
# Check API health
curl http://localhost:8000/health/

# Expected response
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 📞 Support

### Getting Help
- **Documentation**: http://localhost:8000/swagger/
- **API Status**: http://localhost:8000/health/
- **Admin Panel**: http://localhost:8000/admin/

### Contact Information
- **Email**: support@maltacard.com
- **Documentation**: https://docs.maltacard.com
- **GitHub**: https://github.com/maltacard/api

### Feature Requests
Submit feature requests through:
- GitHub Issues
- Support email
- Admin panel feedback

---

## 📚 Additional Resources

### Documentation
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Swagger/OpenAPI](https://swagger.io/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Redis](https://redis.io/documentation)

### Tools
- **API Testing**: Postman, Insomnia
- **Code Generation**: Swagger Codegen
- **Monitoring**: New Relic, DataDog
- **Logging**: ELK Stack, Splunk

### Best Practices
- Always use HTTPS in production
- Implement proper error handling
- Use pagination for large datasets
- Cache frequently accessed data
- Monitor API usage and performance
- Keep dependencies updated
- Implement proper logging
- Use environment variables for configuration

---

**🎉 Congratulations!** You're now ready to integrate with the MaltaCard API. Start with the Quick Start section and gradually explore more advanced features as needed.

**Happy Coding! 🚀** 