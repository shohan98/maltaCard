# MaltaCard API

A comprehensive Django REST API for Malta card management system with token-based authentication and Google OAuth integration.

## 🚀 Features

- **Token-based Authentication** - Secure API authentication using Django REST Framework tokens
- **Google OAuth Integration** - Social login with Google accounts
- **User Management** - Complete user registration, profile management, and authentication
- **Card Management** - Order and manage different types of Malta cards
- **Swagger Documentation** - Interactive API documentation
- **Admin Interface** - Beautiful admin interface with Jazzmin
- **Comprehensive Testing** - Seed data and testing utilities

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Database Seeding](#database-seeding)
- [Admin Interface](#admin-interface)
- [Development](#development)

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Environment Setup

**Important**: This project uses environment variables for sensitive configuration. Follow these steps:

1. **Generate environment file**
   ```bash
   python setup_env.py
   ```

2. **Configure your environment variables**
   Edit the generated `.env` file with your actual values:
   - Email settings for notifications
   - Google OAuth credentials
   - Database configuration (for production)

3. **Security Note**: Never commit your `.env` file to version control!

For detailed environment setup instructions, see [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md).

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd maltaCard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed database with dummy data**
   ```bash
   python manage.py seed_data
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🚀 Quick Start

After installation, you can access:

- **API Documentation**: http://localhost:8000/swagger/
- **Admin Interface**: http://localhost:8000/admin/
- **API Base URL**: http://localhost:8000/api/

### Default Credentials

- **Admin**: `admin` / `admin123`
- **Test User**: `john.doe` / `password123`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints

#### 1. Login
```http
POST /api/auth/auth/login/
Content-Type: application/json

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
        "token": "your-auth-token-here",
        "user_id": 1,
        "username": "john.doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

#### 2. Logout
```http
POST /api/auth/auth/logout/
Authorization: Token your-auth-token-here
```

#### 3. Google OAuth

**Get OAuth URL:**
```http
GET /api/auth/auth/google_login_url/
```

**Handle OAuth Callback:**
```http
POST /api/auth/auth/google_callback/
Content-Type: application/json

{
    "access_token": "google-oauth-access-token"
}
```

### User Management Endpoints

#### 1. Register User
```http
POST /api/auth/users/register/
Content-Type: application/json

{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "New",
    "last_name": "User"
}
```

#### 2. Get Current User
```http
GET /api/auth/users/me/
Authorization: Token your-auth-token-here
```

#### 3. Update User Profile
```http
PATCH /api/auth/profiles/my_profile/
Authorization: Token your-auth-token-here
Content-Type: application/json

{
    "phone_number": "+356 1234 5678",
    "address": "123 Main Street",
    "city": "Valletta",
    "state": "Valletta",
    "postal_code": "VLT 1234",
    "country": "Malta"
}
```

### Card Management Endpoints

#### 1. List Card Types
```http
GET /api/cards/card-types/
```

#### 2. Create Card Order
```http
POST /api/cards/orders/
Authorization: Token your-auth-token-here
Content-Type: application/json

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

#### 3. Get User Orders
```http
GET /api/cards/orders/
Authorization: Token your-auth-token-here
```

## 🔐 Authentication

### Token Authentication

All protected endpoints require a valid authentication token in the header:

```http
Authorization: Token your-auth-token-here
```

### Getting a Token

1. **Login with username/password**
2. **Use the returned token in subsequent requests**

### Google OAuth Flow

1. **Get OAuth URL** from `/api/auth/auth/google_login_url/`
2. **Redirect user** to the returned URL
3. **Handle callback** with the access token
4. **Receive authentication token** for API access

## 🌱 Database Seeding

The application includes comprehensive seed data for development and testing:

```bash
# Seed with default data (10 users, 5 card types, 20 orders)
python manage.py seed_data

# Customize the amount of data
python manage.py seed_data --users 20 --cards 8 --orders 50
```

### Seed Data Includes

- **5 Card Types**: Standard, Premium, Student, Senior, Business
- **10+ Users**: With complete profiles and authentication tokens
- **20+ Orders**: Various statuses and payment methods
- **Admin User**: Ready for admin interface access

## 🎨 Admin Interface

Access the beautiful admin interface at `http://localhost:8000/admin/`

### Features
- **Modern UI** with Jazzmin theme
- **User Management** - View and manage all users
- **Card Management** - Manage card types and orders
- **Order Tracking** - Monitor order status and progress
- **Profile Management** - View and edit user profiles

## 🛠️ Development

### Project Structure

```
maltaCard/
├── authentication/          # User authentication and profiles
│   ├── api_views.py        # API views for authentication
│   ├── serializers.py      # Data serializers
│   ├── models.py           # User profile models
│   └── management/         # Management commands
├── card_management/        # Card and order management
│   ├── api_views.py        # API views for cards
│   ├── models.py           # Card and order models
│   └── serializers.py      # Card serializers
├── core/                   # Core utilities and base models
├── maltaCard/              # Main project settings
└── requirements.txt        # Python dependencies
```

### Available Management Commands

```bash
# Create authentication tokens for existing users
python manage.py create_tokens

# Seed database with dummy data
python manage.py seed_data

# Create superuser
python manage.py createsuperuser
```

### Environment Variables

For production, set these environment variables:

```bash
# Django settings
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com

# Google OAuth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-oauth2-key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-oauth2-secret
```

## 📊 API Response Format

All API responses follow a standardized format:

### Success Response
```json
{
    "success": true,
    "message": "Operation successful",
    "data": {
        // Response data here
    }
}
```

### Error Response
```json
{
    "success": false,
    "message": "Error description",
    "errors": {
        // Validation errors if any
    }
}
```

## 🔧 Configuration

### Google OAuth Setup

1. **Create Google OAuth App** in Google Console
2. **Set redirect URI** to `http://localhost:8000/social-auth/complete/google-oauth2/`
3. **Update settings.py** with your OAuth credentials

### Database Configuration

The default configuration uses SQLite. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'maltacard_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testing

### API Testing

Use the interactive Swagger documentation at `http://localhost:8000/swagger/` to test all endpoints.

### Manual Testing

```bash
# Test login
curl -X POST http://localhost:8000/api/auth/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john.doe", "password": "password123"}'

# Test authenticated endpoint
curl -X GET http://localhost:8000/api/auth/users/me/ \
  -H "Authorization: Token your-token-here"
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Email: contact@maltacard.com
- Documentation: http://localhost:8000/swagger/
- Admin Interface: http://localhost:8000/admin/

---

**MaltaCard API** - Secure, scalable, and user-friendly card management system for Malta.