# MaltaCard API Documentation

## Overview

The MaltaCard API provides a comprehensive REST API for managing Malta card orders, user authentication, and profile management. This document provides detailed information about all available endpoints, request/response formats, and authentication methods.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

The API uses token-based authentication. Include the token in the Authorization header:

```
Authorization: Token your-auth-token-here
```

## Response Format

All API responses follow a standardized format:

### Success Response
```json
{
    "success": true,
    "message": "Operation successful",
    "data": {
        // Response data
    }
}
```

### Error Response
```json
{
    "success": false,
    "message": "Error description",
    "errors": {
        // Validation errors
    }
}
```

## Authentication Endpoints

### 1. Login

**Endpoint:** `POST /api/auth/auth/login/`

**Description:** Authenticate user with username/email and password

**Request Body:**
```json
{
    "username": "john.doe",
    "password": "password123"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
        "user_id": 1,
        "username": "john.doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
- `400 Bad Request` - Validation errors

### 2. Logout

**Endpoint:** `POST /api/auth/auth/logout/`

**Description:** Logout user and delete authentication token

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Response:**
```json
{
    "success": true,
    "message": "Logout successful"
}
```

### 3. Token Authentication

**Endpoint:** `POST /api/auth/token/`

**Description:** Alternative login endpoint using DRF's built-in token authentication

**Request Body:**
```json
{
    "username": "john.doe",
    "password": "password123"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
        "user_id": 1,
        "username": "john.doe",
        "email": "john.doe@example.com"
    }
}
```

### 4. Google OAuth

#### Get OAuth URL

**Endpoint:** `GET /api/auth/auth/google_login_url/`

**Description:** Get Google OAuth authorization URL

**Response:**
```json
{
    "success": true,
    "message": "Google OAuth URL generated",
    "data": {
        "auth_url": "https://accounts.google.com/o/oauth2/auth?..."
    }
}
```

#### Handle OAuth Callback

**Endpoint:** `POST /api/auth/auth/google_callback/`

**Description:** Handle Google OAuth callback and authenticate user

**Request Body:**
```json
{
    "access_token": "google-oauth-access-token"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Google login successful",
    "data": {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
        "user_id": 1,
        "username": "john.doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_google_user": true
    }
}
```

## User Management Endpoints

### 1. Register User

**Endpoint:** `POST /api/auth/users/register/`

**Description:** Register a new user account

**Request Body:**
```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "New",
    "last_name": "User"
}
```

**Response:**
```json
{
    "success": true,
    "message": "User registered successfully",
    "data": {
        "user_id": 2
    }
}
```

### 2. Get Current User

**Endpoint:** `GET /api/auth/users/me/`

**Description:** Get current authenticated user information

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Response:**
```json
{
    "success": true,
    "message": "Current user information",
    "data": {
        "id": 1,
        "username": "john.doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2024-01-15T10:30:00Z",
        "profile": {
            "id": 1,
            "phone_number": "+356 2345 6789",
            "address": "456 Main Street",
            "city": "Sliema",
            "state": "Sliema",
            "postal_code": "SLM 2345",
            "country": "Malta",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "is_active": true
        }
    }
}
```

### 3. List Users (Admin Only)

**Endpoint:** `GET /api/auth/users/`

**Description:** List all users (admin only)

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Query Parameters:**
- `username` - Filter by username (contains)
- `email` - Filter by email (contains)
- `first_name` - Filter by first name (contains)
- `last_name` - Filter by last name (contains)
- `date_joined_after` - Filter by date joined (after)
- `date_joined_before` - Filter by date joined (before)
- `search` - Search across username, email, first_name, last_name
- `ordering` - Order by field (prefix with - for descending)

**Response:**
```json
{
    "success": true,
    "message": "Users retrieved successfully",
    "data": [
        {
            "id": 1,
            "username": "john.doe",
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "date_joined": "2024-01-15T10:30:00Z",
            "profile": {
                "id": 1,
                "phone_number": "+356 2345 6789",
                "address": "456 Main Street",
                "city": "Sliema",
                "state": "Sliema",
                "postal_code": "SLM 2345",
                "country": "Malta",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
                "is_active": true
            }
        }
    ],
    "pagination": {
        "count": 10,
        "next": "http://localhost:8000/api/auth/users/?page=2",
        "previous": null,
        "results": 10
    }
}
```

## User Profile Endpoints

### 1. Get My Profile

**Endpoint:** `GET /api/auth/profiles/my_profile/`

**Description:** Get current user's profile

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Response:**
```json
{
    "success": true,
    "message": "User profile",
    "data": {
        "id": 1,
        "phone_number": "+356 2345 6789",
        "address": "456 Main Street",
        "city": "Sliema",
        "state": "Sliema",
        "postal_code": "SLM 2345",
        "country": "Malta",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "is_active": true
    }
}
```

### 2. Update My Profile

**Endpoint:** `PATCH /api/auth/profiles/my_profile/`

**Description:** Update current user's profile

**Headers:**
```
Authorization: Token your-auth-token-here
Content-Type: application/json
```

**Request Body:**
```json
{
    "phone_number": "+356 1234 5678",
    "address": "123 Main Street",
    "city": "Valletta",
    "state": "Valletta",
    "postal_code": "VLT 1234",
    "country": "Malta"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Profile updated successfully",
    "data": {
        "id": 1,
        "phone_number": "+356 1234 5678",
        "address": "123 Main Street",
        "city": "Valletta",
        "state": "Valletta",
        "postal_code": "VLT 1234",
        "country": "Malta",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T11:00:00Z",
        "is_active": true
    }
}
```

## Card Management Endpoints

### 1. List Card Types

**Endpoint:** `GET /api/cards/card-types/`

**Description:** List all available card types

**Response:**
```json
{
    "success": true,
    "message": "Card types retrieved successfully",
    "data": [
        {
            "id": 1,
            "name": "Standard Malta Card",
            "description": "Basic Malta identification card with standard features",
            "price": "25.00",
            "validity_period": 5,
            "features": "Basic identification, photo, personal details",
            "is_active": true,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

### 2. Get Card Type Details

**Endpoint:** `GET /api/cards/card-types/{id}/`

**Description:** Get specific card type details

**Response:**
```json
{
    "success": true,
    "message": "Card type details",
    "data": {
        "id": 1,
        "name": "Standard Malta Card",
        "description": "Basic Malta identification card with standard features",
        "price": "25.00",
        "validity_period": 5,
        "features": "Basic identification, photo, personal details",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

### 3. Create Card Order

**Endpoint:** `POST /api/cards/orders/`

**Description:** Create a new card order

**Headers:**
```
Authorization: Token your-auth-token-here
Content-Type: application/json
```

**Request Body:**
```json
{
    "card_type": 1,
    "quantity": 2,
    "delivery_address": "123 Main Street",
    "delivery_city": "Valletta",
    "delivery_postal_code": "VLT 1234",
    "payment_method": "credit_card",
    "special_instructions": "Handle with care"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Order created successfully",
    "data": {
        "id": 1,
        "user": 1,
        "card_type": 1,
        "quantity": 2,
        "total_amount": "50.00",
        "status": "pending",
        "payment_method": "credit_card",
        "order_date": "2024-01-15T10:30:00Z",
        "delivery_address": "123 Main Street",
        "delivery_city": "Valletta",
        "delivery_postal_code": "VLT 1234",
        "special_instructions": "Handle with care",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

### 4. List My Orders

**Endpoint:** `GET /api/cards/orders/`

**Description:** List current user's orders

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Query Parameters:**
- `status` - Filter by order status
- `payment_method` - Filter by payment method
- `order_date_after` - Filter by order date (after)
- `order_date_before` - Filter by order date (before)
- `search` - Search across order fields
- `ordering` - Order by field (prefix with - for descending)

**Response:**
```json
{
    "success": true,
    "message": "Orders retrieved successfully",
    "data": [
        {
            "id": 1,
            "user": 1,
            "card_type": {
                "id": 1,
                "name": "Standard Malta Card",
                "price": "25.00"
            },
            "quantity": 2,
            "total_amount": "50.00",
            "status": "pending",
            "payment_method": "credit_card",
            "order_date": "2024-01-15T10:30:00Z",
            "delivery_address": "123 Main Street",
            "delivery_city": "Valletta",
            "delivery_postal_code": "VLT 1234",
            "special_instructions": "Handle with care",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ],
    "pagination": {
        "count": 5,
        "next": null,
        "previous": null,
        "results": 5
    }
}
```

### 5. Get Order Details

**Endpoint:** `GET /api/cards/orders/{id}/`

**Description:** Get specific order details

**Headers:**
```
Authorization: Token your-auth-token-here
```

**Response:**
```json
{
    "success": true,
    "message": "Order details",
    "data": {
        "id": 1,
        "user": 1,
        "card_type": {
            "id": 1,
            "name": "Standard Malta Card",
            "description": "Basic Malta identification card with standard features",
            "price": "25.00",
            "validity_period": 5,
            "features": "Basic identification, photo, personal details"
        },
        "quantity": 2,
        "total_amount": "50.00",
        "status": "pending",
        "payment_method": "credit_card",
        "order_date": "2024-01-15T10:30:00Z",
        "delivery_address": "123 Main Street",
        "delivery_city": "Valletta",
        "delivery_postal_code": "VLT 1234",
        "special_instructions": "Handle with care",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "cards": [
            {
                "id": 1,
                "card_number": "MC00000101",
                "status": "active",
                "issue_date": "2024-01-16T10:30:00Z",
                "expiry_date": "2029-01-16T10:30:00Z"
            }
        ]
    }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Validation errors |
| 401 | Unauthorized - Invalid credentials or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 1000 requests per hour per IP address
- 100 requests per minute per authenticated user

## Pagination

List endpoints support pagination with the following parameters:
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10, max: 100)

## Filtering and Search

Most list endpoints support filtering and search:

### Common Filters
- `search` - Search across relevant fields
- `ordering` - Order by field (prefix with - for descending)

### Date Filters
- `created_at_after` - Filter by creation date (after)
- `created_at_before` - Filter by creation date (before)
- `updated_at_after` - Filter by update date (after)
- `updated_at_before` - Filter by update date (before)

## Testing

### Using Swagger UI

Access the interactive API documentation at:
```
http://localhost:8000/swagger/
```

### Using curl

```bash
# Login
curl -X POST http://localhost:8000/api/auth/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john.doe", "password": "password123"}'

# Get user profile
curl -X GET http://localhost:8000/api/auth/users/me/ \
  -H "Authorization: Token your-token-here"

# Create order
curl -X POST http://localhost:8000/api/cards/orders/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "card_type": 1,
    "quantity": 2,
    "delivery_address": "123 Main Street",
    "delivery_city": "Valletta",
    "delivery_postal_code": "VLT 1234",
    "payment_method": "credit_card"
  }'
```

## SDKs and Libraries

### Python
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/auth/login/', json={
    'username': 'john.doe',
    'password': 'password123'
})
token = response.json()['data']['token']

# Make authenticated request
headers = {'Authorization': f'Token {token}'}
response = requests.get('http://localhost:8000/api/auth/users/me/', headers=headers)
```

### JavaScript
```javascript
// Login
const response = await fetch('http://localhost:8000/api/auth/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'john.doe',
        password: 'password123'
    })
});
const data = await response.json();
const token = data.data.token;

// Make authenticated request
const profileResponse = await fetch('http://localhost:8000/api/auth/users/me/', {
    headers: {
        'Authorization': `Token ${token}`
    }
});
```

## Support

For API support and questions:
- Email: contact@maltacard.com
- Documentation: http://localhost:8000/swagger/
- Admin Interface: http://localhost:8000/admin/ 