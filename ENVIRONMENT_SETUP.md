# Environment Variables Setup

This project uses environment variables to manage sensitive configuration data. Follow these steps to set up your environment:

## 1. Install Dependencies

First, install the required packages:

```bash
pip install -r requirements.txt
```

## 2. Create Your Environment File

Copy the example environment file and create your own `.env` file:

```bash
cp env.example .env
```

## 3. Configure Your Environment Variables

Edit the `.env` file with your actual values:

### Django Settings
```bash
# Generate a new secret key for production
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Settings
```bash
DATABASE_URL=sqlite:///db.sqlite3
```

### Email Settings
```bash
# For development (emails will be printed to console)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# For production (uncomment and configure)
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@maltacard.com
```

### Google OAuth Settings
```bash
# Get these from Google Cloud Console
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-oauth2-key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-oauth2-secret
```

### Security Settings
```bash
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

## 4. Generate a New Secret Key

For production, generate a new Django secret key:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## 5. Security Best Practices

- **Never commit your `.env` file** to version control
- **Use different values** for development and production
- **Rotate secrets regularly** in production
- **Use strong, unique passwords** for all services
- **Enable 2FA** on your Google Cloud Console account

## 6. Production Deployment

For production deployment:

1. Set `DEBUG=False`
2. Use a proper database (PostgreSQL, MySQL)
3. Configure proper email backend
4. Set up HTTPS and update `CSRF_TRUSTED_ORIGINS`
5. Use environment-specific secret keys
6. Configure proper logging

## 7. Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generated fallback |
| `DEBUG` | Debug mode | True |
| `ALLOWED_HOSTS` | Allowed hosts | localhost,127.0.0.1 |
| `EMAIL_BACKEND` | Email backend | console |
| `EMAIL_HOST` | SMTP host | smtp.gmail.com |
| `EMAIL_PORT` | SMTP port | 587 |
| `EMAIL_USE_TLS` | Use TLS | True |
| `EMAIL_HOST_USER` | Email username | your-email@gmail.com |
| `EMAIL_HOST_PASSWORD` | Email password | your-app-password |
| `DEFAULT_FROM_EMAIL` | Default from email | noreply@maltacard.com |
| `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` | Google OAuth key | your-google-oauth2-key |
| `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` | Google OAuth secret | your-google-oauth2-secret |
| `CSRF_TRUSTED_ORIGINS` | CSRF trusted origins | http://localhost:8000,http://127.0.0.1:8000 | 