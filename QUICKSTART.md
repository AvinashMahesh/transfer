# Quick Start Guide

## Get Started in 5 Minutes

This guide will get you up and running with the Deloitte Initiative Discovery Platform API.

---

## Prerequisites

- Docker & Docker Compose installed
- OR Python 3.11+ and PostgreSQL 15+

---

## Option 1: Docker (Recommended)

### Step 1: Start Services

```bash
docker-compose up -d
```

This starts:
- FastAPI application (port 8000)
- PostgreSQL database (port 5432)
- Qdrant vector database (port 6333)

### Step 2: Access Swagger UI

Open in your browser:
```
http://localhost:8000/docs
```

### Step 3: Test the API

1. Click on `/api/v1/auth/login`
2. Click "Try it out"
3. Use this JSON:
   ```json
   {
     "email": "analyst@deloitte.com",
     "password": "password123"
   }
   ```
4. Click "Execute"
5. Copy the `access_token` from the response

### Step 4: Authorize

1. Click the "Authorize" button at the top
2. Enter: `Bearer <your-token>`
3. Click "Authorize"

Now you can test all protected endpoints!

---

## Option 2: Local Python

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set your PostgreSQL connection:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/deloitte_initiatives
```

### Step 3: Run Server

```bash
python run.py
```

### Step 4: Access API

Open: http://localhost:8000/docs

---

## Sample Data

The system includes pre-loaded test data:

### Users

| Email | Password | Role |
|-------|----------|------|
| analyst@deloitte.com | password123 | Analyst |
| leader@deloitte.com | password123 | Leader |
| admin@deloitte.com | password123 | Admin |

### Sample Initiatives

1. **AI Healthcare Research Pod** (Technology)
2. **Innovation Hub - GenAI Applications** (Technology)
3. **Financial Services Digital Transformation** (Strategy)
4. **Sustainability Volunteering** (Risk & Sustainability)

---

## Common Tasks

### 1. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "analyst@deloitte.com",
    "password": "password123"
  }'
```

### 2. Get Your Profile

```bash
curl "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer <token>"
```

### 3. Search Initiatives

```bash
curl "http://localhost:8000/api/v1/search?q=AI"
```

### 4. Get Recommendations

```bash
curl "http://localhost:8000/api/v1/recommendations" \
  -H "Authorization: Bearer <token>"
```

### 5. Save an Initiative

```bash
curl -X POST "http://localhost:8000/api/v1/engagement/save" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"initiative_id": 1}'
```

---

## Explore the API

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
  - Try all endpoints interactively
  - See request/response schemas
  - Test with sample data

- **ReDoc**: http://localhost:8000/redoc
  - Beautiful API documentation
  - Detailed descriptions
  - Code samples

### API Endpoints Overview

```
Authentication    → /api/v1/auth/*
User Management   → /api/v1/users/*
Initiatives       → /api/v1/initiatives/*
Search           → /api/v1/search/*
Recommendations  → /api/v1/recommendations/*
Engagement       → /api/v1/engagement/*
```

---

## Troubleshooting

### Port Already in Use

```bash
# Stop services
docker-compose down

# Or kill process on port 8000
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres
```

### Module Not Found

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## Next Steps

1. ✅ API is running
2. ✅ Test with sample data
3. 📖 Read full docs: `API_DOCUMENTATION.md`
4. 🏗️ Check architecture: `ARCHITECTURE.md`
5. 🚀 Deploy: `DEPLOYMENT_GUIDE.md`

---

## Support

- **Swagger UI**: http://localhost:8000/docs
- **Documentation**: See `README.md`
- **API Reference**: See `API_DOCUMENTATION.md`

---

**You're all set! Start exploring the API 🚀**