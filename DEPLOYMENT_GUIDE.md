# Deployment Guide

## Deloitte Initiative Discovery Platform - Backend Deployment

This guide covers deployment options for the backend API.

---

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Azure App Service](#azure-app-service)
4. [Database Setup](#database-setup)
5. [Environment Configuration](#environment-configuration)
6. [Production Checklist](#production-checklist)

---

## 1. Local Development

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- pip and virtualenv

### Steps

```bash
# 1. Clone repository
git clone <repository-url>
cd workspace

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Run the application
python run.py
```

The API will be available at http://localhost:8000

### Database Initialization

The application automatically creates tables and seeds sample data on first run.

To manually initialize:

```bash
python -c "from app.core.init_db import init_db, seed_sample_data; init_db(); seed_sample_data()"
```

---

## 2. Docker Deployment

### Quick Start with Docker Compose

```bash
# Start all services (API, PostgreSQL, Qdrant)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Stop and remove volumes (clears data)
docker-compose down -v
```

### Services Included

- **API**: FastAPI application on port 8000
- **PostgreSQL**: Database on port 5432
- **Qdrant**: Vector database on port 6333

### Custom Docker Build

```bash
# Build image
docker build -t deloitte-initiatives-api:latest .

# Run container
docker run -d \
  --name deloitte-api \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e SECRET_KEY="your-secret-key" \
  deloitte-initiatives-api:latest

# View logs
docker logs -f deloitte-api

# Stop container
docker stop deloitte-api
docker rm deloitte-api
```

---

## 3. Azure App Service

### Prerequisites

- Azure CLI installed
- Azure subscription
- Resource group created

### Deployment Steps

#### Option A: Using Azure CLI

```bash
# 1. Login to Azure
az login

# 2. Create App Service Plan
az appservice plan create \
  --name deloitte-initiatives-plan \
  --resource-group deloitte-rg \
  --sku B1 \
  --is-linux

# 3. Create Web App
az webapp create \
  --resource-group deloitte-rg \
  --plan deloitte-initiatives-plan \
  --name deloitte-initiatives-api \
  --runtime "PYTHON:3.11"

# 4. Configure environment variables
az webapp config appsettings set \
  --resource-group deloitte-rg \
  --name deloitte-initiatives-api \
  --settings \
    DATABASE_URL="<your-db-url>" \
    SECRET_KEY="<your-secret>" \
    AZURE_AD_TENANT_ID="<tenant-id>" \
    AZURE_AD_CLIENT_ID="<client-id>" \
    AZURE_AD_CLIENT_SECRET="<client-secret>"

# 5. Deploy code
az webapp up \
  --name deloitte-initiatives-api \
  --resource-group deloitte-rg
```

#### Option B: Using GitHub Actions

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'deloitte-initiatives-api'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

### Azure Database for PostgreSQL

```bash
# Create PostgreSQL server
az postgres flexible-server create \
  --resource-group deloitte-rg \
  --name deloitte-db-server \
  --location eastus \
  --admin-user dbadmin \
  --admin-password <secure-password> \
  --sku-name Standard_B1ms \
  --version 15

# Create database
az postgres flexible-server db create \
  --resource-group deloitte-rg \
  --server-name deloitte-db-server \
  --database-name deloitte_initiatives

# Configure firewall (allow Azure services)
az postgres flexible-server firewall-rule create \
  --resource-group deloitte-rg \
  --name deloitte-db-server \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

Get connection string:
```
postgresql://dbadmin:<password>@deloitte-db-server.postgres.database.azure.com:5432/deloitte_initiatives
```

---

## 4. Database Setup

### PostgreSQL Installation

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### macOS

```bash
brew install postgresql@15
brew services start postgresql@15
```

#### Windows

Download and install from: https://www.postgresql.org/download/windows/

### Create Database

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE deloitte_initiatives;
CREATE USER deloitte_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE deloitte_initiatives TO deloitte_user;
\q
```

### Database Migration (Future)

Alembic is included for database migrations:

```bash
# Initialize migrations (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 5. Environment Configuration

### Development Environment

`.env` file:

```env
# Application
APP_NAME=Deloitte Initiative Discovery Platform
APP_VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=postgresql://deloitte_user:password@localhost:5432/deloitte_initiatives

# Authentication
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Vector Database
QDRANT_URL=http://localhost:6333
```

### Production Environment

`.env.production`:

```env
# Application
APP_NAME=Deloitte Initiative Discovery Platform
APP_VERSION=1.0.0
DEBUG=False

# Database (Azure PostgreSQL)
DATABASE_URL=postgresql://user:pass@server.postgres.database.azure.com:5432/db?sslmode=require

# Authentication
SECRET_KEY=<generate-strong-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Azure AD B2C
AZURE_AD_TENANT_ID=<your-tenant-id>
AZURE_AD_CLIENT_ID=<your-client-id>
AZURE_AD_CLIENT_SECRET=<your-client-secret>
AZURE_AD_AUTHORITY=https://login.microsoftonline.com/<tenant-id>

# Vector Database (Qdrant Cloud)
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=<your-api-key>
```

### Generating Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 6. Production Checklist

### Security

- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set `DEBUG=False`
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly (restrict origins)
- [ ] Enable rate limiting
- [ ] Implement request logging
- [ ] Set up WAF (Web Application Firewall)
- [ ] Regular security audits

### Database

- [ ] Enable SSL/TLS connections
- [ ] Set up automated backups
- [ ] Configure connection pooling
- [ ] Optimize indexes
- [ ] Set up monitoring
- [ ] Plan for scaling (read replicas)

### Authentication

- [ ] Integrate Azure AD B2C
- [ ] Configure proper token expiration
- [ ] Implement refresh tokens
- [ ] Set up audit logging

### Performance

- [ ] Enable caching (Redis)
- [ ] Configure CDN for static assets
- [ ] Set up load balancer
- [ ] Optimize database queries
- [ ] Enable compression
- [ ] Monitor response times

### Monitoring

- [ ] Set up Application Insights (Azure)
- [ ] Configure error tracking (Sentry)
- [ ] Set up logging aggregation
- [ ] Create alerting rules
- [ ] Monitor API metrics
- [ ] Set up health checks

### Backup & Recovery

- [ ] Automated database backups
- [ ] Backup retention policy
- [ ] Disaster recovery plan
- [ ] Test restore procedures
- [ ] Document recovery steps

### Documentation

- [ ] API documentation up to date
- [ ] Deployment procedures documented
- [ ] Runbook for common issues
- [ ] Contact information for support
- [ ] Architecture diagrams current

---

## Health Checks

### API Health

```bash
# Check API status
curl http://localhost:8000/health

# Expected response
{"status": "healthy"}
```

### Database Connection

```bash
# Test database connection
python -c "
from app.core.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connection: OK')
"
```

---

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### Database Connection Failed

Check:
1. PostgreSQL service is running
2. Database exists
3. Credentials are correct
4. Firewall allows connection
5. SSL mode is appropriate

#### Module Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### Docker Issues

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## Support

For deployment issues:

1. Check logs: `docker-compose logs -f` or Azure App Service logs
2. Verify environment variables
3. Test database connectivity
4. Review error messages
5. Contact DevOps team

---

## Additional Resources

- [FastAPI Deployment Docs](https://fastapi.tiangolo.com/deployment/)
- [Azure App Service Docs](https://docs.microsoft.com/en-us/azure/app-service/)
- [PostgreSQL Azure Docs](https://docs.microsoft.com/en-us/azure/postgresql/)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated**: December 2, 2025