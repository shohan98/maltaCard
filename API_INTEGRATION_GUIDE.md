# 🚀 MaltaCard API Integration Guide

## Quick Start

### 1. Get Your API Token
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password",
    "password_confirm": "your-password",
    "first_name": "Your",
    "last_name": "Name"
  }'

# Login to get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password"
  }'
```

### 2. Use Your Token
```bash
# All API calls require this header
Authorization: Token your-token-here
```

## 🔐 Authentication

### Token Format
```bash
Authorization: Token your-token-here
```

### Token Management
```bash
# Refresh token
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Authorization: Token your-token"

# Logout
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token your-token"
```

## 📡 API Endpoints

### Card Types
```bash
# List all card types
GET /api/cards/card-types/

# Get popular card types
GET /api/cards/card-types/popular/

# Filter by price range
GET /api/cards/card-types/price_range/?min_price=10&max_price=50

# Create card type
POST /api/cards/card-types/
```

### Cards
```bash
# List all cards
GET /api/cards/cards/

# Get virtual cards only
GET /api/cards/cards/virtual_cards/

# Get physical cards only
GET /api/cards/cards/physical_cards/

# Filter by price range
GET /api/cards/cards/by_price_range/?min_price=10&max_price=50
```

### Orders
```bash
# Create new order
POST /api/cards/orders/

# Get user's orders
GET /api/cards/orders/my_orders/

# Cancel order
POST /api/cards/orders/{id}/cancel_order/

# Update order status
POST /api/cards/orders/{id}/update_status/
```

## 📝 Request Examples

### Create Order
```bash
curl -X POST http://localhost:8000/api/cards/orders/ \
  -H "Authorization: Token your-token" \
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

### Get Card Types
```bash
curl -X GET http://localhost:8000/api/cards/card-types/ \
  -H "Authorization: Token your-token"
```

### Get User's Orders
```bash
curl -X GET http://localhost:8000/api/cards/orders/my_orders/ \
  -H "Authorization: Token your-token"
```

## 🔍 Query Parameters

### Pagination
```bash
GET /api/cards/card-types/?page=1&page_size=20
```

### Search
```bash
GET /api/cards/card-types/?search=premium
```

### Filtering
```bash
# Price range
GET /api/cards/card-types/?price_min=10&price_max=50

# Duration type
GET /api/cards/card-types/?duration_type=monthly

# Popular cards
GET /api/cards/card-types/?is_popular=true

# Order status
GET /api/cards/orders/?status=pending
```

### Sorting
```bash
# Ascending
GET /api/cards/card-types/?ordering=price

# Descending
GET /api/cards/card-types/?ordering=-price
```

## ❌ Error Handling

### Common Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limited

### Error Response Format
```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field_name": ["Specific error"]
  },
  "status_code": 400
}
```

## 🛠️ SDK Examples

### JavaScript (Axios)
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

  async getCardTypes() {
    const response = await this.client.get('/api/cards/card-types/');
    return response.data;
  }

  async createOrder(orderData) {
    const response = await this.client.post('/api/cards/orders/', orderData);
    return response.data;
  }

  async getMyOrders() {
    const response = await this.client.get('/api/cards/orders/my_orders/');
    return response.data;
  }
}

// Usage
const api = new MaltaCardAPI('http://localhost:8000', 'your-token');
const cardTypes = await api.getCardTypes();
```

### Python (Requests)
```python
import requests

class MaltaCardAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }

    def get_card_types(self):
        response = requests.get(
            f'{self.base_url}/api/cards/card-types/',
            headers=self.headers
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

# Usage
api = MaltaCardAPI('http://localhost:8000', 'your-token')
card_types = api.get_card_types()
```

## 🧪 Testing

### Test Environment
```bash
# Development
http://localhost:8000/api/

# Swagger Documentation
http://localhost:8000/swagger/
```

### Quick Test
```bash
# 1. Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# 3. Test API
curl -X GET http://localhost:8000/api/cards/card-types/ \
  -H "Authorization: Token your-token"
```

## ⚡ Rate Limiting

- **API endpoints**: 10 requests/second
- **Auth endpoints**: 5 requests/minute
- **Admin endpoints**: 2 requests/second

## 🔧 Troubleshooting

### Common Issues

1. **401 Unauthorized**
   - Check token is included in headers
   - Verify token is valid
   - Re-login to get new token

2. **403 CSRF Error**
   - API doesn't use CSRF tokens
   - Use token authentication only

3. **429 Rate Limited**
   - Reduce request frequency
   - Implement exponential backoff

4. **500 Server Error**
   - Check server logs
   - Verify database connection

### Health Check
```bash
curl http://localhost:8000/health/
```

## 📞 Support

- **Documentation**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health/

## 🚀 Production

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-production-secret
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:port/db
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Docker Deployment
```bash
# Build and start
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

---

**🎉 Ready to integrate!** Start with the Quick Start section and explore the API endpoints.

**Happy Coding! 🚀** 