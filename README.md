# 🚀 MaltaCard - Card Management System

A comprehensive Django-based card management system with REST API, email notifications, and Docker support.

## 🎯 Features

- **🔐 Email-based Authentication** - No usernames, fully email-based auth
- **🃏 Card Management** - Virtual and physical card types
- **📦 Order System** - Complete order lifecycle management
- **📧 Email Notifications** - Order confirmations and status updates
- **🔌 REST API** - Full API with Swagger documentation
- **🐳 Docker Support** - Production-ready Docker setup
- **📊 Admin Interface** - Django admin with custom styling
- **🔍 Search & Filtering** - Advanced search and filtering capabilities
- **📱 Responsive Design** - Mobile-friendly interface

## 🚀 Quick Start

### For New Developers (macOS)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd maltaCard
   ```

2. **Run the setup script**
   ```bash
   ./setup.sh
   ```

   This script will automatically:
   - ✅ Install required tools (Homebrew, Python 3.13, Git, Docker)
   - ✅ Create virtual environment
   - ✅ Install Python dependencies
   - ✅ Set up environment variables
   - ✅ Run database migrations
   - ✅ Create superuser (optional)
   - ✅ Start development server

3. **Access the application**
   - **Main App**: http://localhost:8000/
   - **Admin Panel**: http://localhost:8000/admin/
   - **API Docs**: http://localhost:8000/swagger/
   - **API Endpoints**: http://localhost:8000/api/

### Manual Setup (Other Platforms)

1. **Install Python 3.13**
   ```bash
   # macOS
   brew install python@3.13
   
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.13 python3.13-venv
   ```

2. **Create virtual environment**
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start server**
   ```bash
   python manage.py runserver
   ```

## 🐳 Docker Setup

### Development
```bash
# Build and start services
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Production
```bash
# Start with nginx
docker-compose --profile production up -d
```

## 📡 API Documentation

### Quick API Test
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

### API Endpoints

#### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get token
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/me/` - Get current user

#### Card Types
- `GET /api/cards/card-types/` - List all card types
- `POST /api/cards/card-types/` - Create card type
- `GET /api/cards/card-types/popular/` - Get popular cards
- `GET /api/cards/card-types/price_range/` - Filter by price

#### Cards
- `GET /api/cards/cards/` - List all cards
- `GET /api/cards/cards/virtual_cards/` - Virtual cards only
- `GET /api/cards/cards/physical_cards/` - Physical cards only

#### Orders
- `POST /api/cards/orders/` - Create order
- `GET /api/cards/orders/my_orders/` - User's orders
- `POST /api/cards/orders/{id}/cancel_order/` - Cancel order

## 📁 Project Structure

```
maltaCard/
├── authentication/          # User authentication
│   ├── models.py           # Custom user model
│   ├── serializers.py      # API serializers
│   ├── api_views.py        # API views
│   └── backends.py         # Email authentication
├── card_management/         # Card and order management
│   ├── models.py           # Card, CardType, CardOrder
│   ├── serializers.py      # Order serializers
│   ├── api_views.py        # Card API views
│   └── signals.py          # Email notifications
├── core/                   # Core utilities
│   ├── models.py           # Base models
│   ├── viewsets.py         # Base viewset
│   ├── utils.py            # Utilities
│   └── middleware.py       # CSRF middleware
├── maltaCard/              # Django settings
│   ├── settings.py         # Main settings
│   ├── urls.py             # URL configuration
│   └── production.py       # Production settings
├── templates/              # Email templates
├── static/                 # Static files
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker services
├── setup.sh               # macOS setup script
└── requirements.txt        # Python dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DATABASE_URL=sqlite:///db.sqlite3

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Google OAuth Settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-oauth2-key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-oauth2-secret

# Security Settings
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### Email Configuration

For Gmail:
1. Enable 2-Step Verification
2. Generate App Password
3. Update `.env` with your credentials

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### API Testing
```bash
# Test email functionality
python manage.py test_email --email your-email@example.com

# Test card orders
python manage.py recalculate_card_orders
```

### Manual Testing
```bash
# Start server
python manage.py runserver

# Access URLs
# http://localhost:8000/admin/     # Admin panel
# http://localhost:8000/swagger/   # API docs
# http://localhost:8000/api/       # API endpoints
```

## 📊 Database

### Models
- **CustomUser** - Email-based user authentication
- **UserProfile** - Extended user information
- **CardType** - Card categories and pricing
- **Card** - Individual card instances
- **CardOrder** - Order management

### Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development)
rm db.sqlite3
python manage.py migrate
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up SSL certificates
- [ ] Configure email settings
- [ ] Set secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up monitoring

### Docker Production
```bash
# Build production image
docker-compose --profile production build

# Start production services
docker-compose --profile production up -d

# Check logs
docker-compose logs -f
```

## 🔍 Troubleshooting

### Common Issues

1. **Virtual Environment**
   ```bash
   # Recreate virtual environment
   rm -rf .venv
   python3.13 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Database Issues**
   ```bash
   # Reset database
   rm db.sqlite3
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Email Issues**
   ```bash
   # Test email configuration
   python manage.py test_email --email your-email@example.com
   ```

4. **Docker Issues**
   ```bash
   # Rebuild containers
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

### Health Checks
```bash
# Check Django setup
python manage.py check

# Check API health
curl http://localhost:8000/health/

# Check Docker services
docker-compose ps
```

## 📚 Documentation

- [API Integration Guide](API_INTEGRATION_GUIDE.md) - Complete API documentation
- [Docker Deployment Guide](DOCKER_DEPLOYMENT.md) - Docker setup and deployment
- [Swagger Documentation](http://localhost:8000/swagger/) - Interactive API docs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

- **Documentation**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health/

---

**🎉 Welcome to MaltaCard!** Start with the setup script and explore the API documentation.

**Happy Coding! 🚀**