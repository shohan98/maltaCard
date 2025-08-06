# Docker Deployment Guide for MaltaCard

This guide explains how to deploy the MaltaCard Django application using Docker and Docker Compose.

## Prerequisites

- Docker
- Docker Compose
- Git

## Quick Start

### 1. Clone the repository
```bash
git clone <repository-url>
cd maltaCard
```

### 2. Create environment file
Create a `.env` file in the project root:
```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings
POSTGRES_DB=maltacard
POSTGRES_USER=maltacard_user
POSTGRES_PASSWORD=maltacard_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis Settings
REDIS_URL=redis://redis:6379/0

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=shohan.plan@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=shohan.plan@gmail.com

# Security Settings
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### 3. Build and run with Docker Compose
```bash
# Build the images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the application
- **Django Admin**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/swagger/
- **API Base URL**: http://localhost:8000/api/

## Production Deployment

### 1. With Nginx (Recommended)
```bash
# Start with nginx
docker-compose --profile production up -d
```

This will start:
- Django application (port 8000)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Nginx reverse proxy (port 80)

### 2. Environment-specific configurations

#### Development
```bash
docker-compose up -d
```

#### Production
```bash
docker-compose --profile production up -d
```

## Services Overview

### Web Application (`web`)
- **Port**: 8000
- **Image**: Built from Dockerfile
- **Dependencies**: Database and Redis
- **Health Check**: Available at `/admin/`

### PostgreSQL Database (`db`)
- **Port**: 5432
- **Image**: postgres:15
- **Data**: Persisted in `postgres_data` volume
- **Health Check**: Database connectivity

### Redis Cache (`redis`)
- **Port**: 6379
- **Image**: redis:7-alpine
- **Data**: Persisted in `redis_data` volume
- **Health Check**: Redis ping

### Nginx Reverse Proxy (`nginx`)
- **Port**: 80
- **Image**: nginx:alpine
- **Features**:
  - Rate limiting
  - Gzip compression
  - Security headers
  - Static file serving
  - SSL termination (if configured)

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django secret key | Required |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1,0.0.0.0` |
| `POSTGRES_DB` | Database name | `maltacard` |
| `POSTGRES_USER` | Database user | `maltacard_user` |
| `POSTGRES_PASSWORD` | Database password | `maltacard_password` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |
| `EMAIL_HOST_USER` | Email sender | `shohan.plan@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Email password | Required |

### Database Migration

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Load initial data (if any)
docker-compose exec web python manage.py loaddata initial_data.json
```

### Static Files

Static files are automatically collected and served by Nginx:

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## Monitoring and Logs

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f redis
```

### Health checks
```bash
# Check service health
docker-compose ps

# Test application health
curl http://localhost:8000/health/
```

## Backup and Restore

### Database backup
```bash
# Create backup
docker-compose exec db pg_dump -U maltacard_user maltacard > backup.sql

# Restore backup
docker-compose exec -T db psql -U maltacard_user maltacard < backup.sql
```

### Volume backup
```bash
# Backup volumes
docker run --rm -v maltaCard_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
docker run --rm -v maltaCard_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis_backup.tar.gz -C /data .
```

## Troubleshooting

### Common Issues

1. **Database connection failed**
   ```bash
   # Check database logs
   docker-compose logs db
   
   # Restart database
   docker-compose restart db
   ```

2. **Static files not loading**
   ```bash
   # Recollect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

3. **Email not working**
   - Check Gmail app password configuration
   - Verify email settings in `.env` file

4. **Port conflicts**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Change port in docker-compose.yml
   ports:
     - "8001:8000"  # Use port 8001 instead
   ```

### Performance Optimization

1. **Database optimization**
   ```bash
   # Add database indexes
   docker-compose exec web python manage.py dbshell
   ```

2. **Cache optimization**
   ```bash
   # Clear cache
   docker-compose exec web python manage.py cache_clear
   ```

3. **Static file optimization**
   ```bash
   # Compress static files
   docker-compose exec web python manage.py compress
   ```

## Security Considerations

1. **Change default passwords**
   - Update `POSTGRES_PASSWORD` in `.env`
   - Use strong passwords for all services

2. **SSL/TLS configuration**
   - Configure SSL certificates for production
   - Update nginx.conf with SSL settings

3. **Firewall configuration**
   - Only expose necessary ports
   - Use reverse proxy for external access

4. **Regular updates**
   ```bash
   # Update images
   docker-compose pull
   docker-compose up -d
   ```

## Scaling

### Horizontal scaling
```bash
# Scale web service
docker-compose up -d --scale web=3
```

### Load balancing
- Configure nginx for load balancing
- Use external load balancer (AWS ALB, etc.)

## Maintenance

### Regular tasks
```bash
# Update dependencies
docker-compose exec web pip install --upgrade -r requirements.txt

# Database maintenance
docker-compose exec db vacuumdb -U maltacard_user maltacard

# Log rotation
docker-compose exec web logrotate /etc/logrotate.conf
```

### Monitoring
- Set up monitoring with Prometheus/Grafana
- Configure alerting for service failures
- Monitor resource usage

## Support

For issues and questions:
- Check logs: `docker-compose logs`
- Review configuration files
- Test individual services
- Consult Django documentation 