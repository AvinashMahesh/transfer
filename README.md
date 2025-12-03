# Deloitte Initiative Discovery Platform - Backend

A unified backend platform for Deloitte analysts to discover and engage with firm initiatives, powered by AI-driven recommendations.

## 🚀 Overview

The Deloitte Initiative Discovery Platform addresses the challenge of scattered information about firm initiatives (research pods, innovation hubs, volunteering opportunities, etc.) by providing:

- **Unified Initiative Catalog**: Browse all firm initiatives in one place
- **AI-Powered Recommendations**: Personalized suggestions based on skills and interests
- **Smart Search**: Semantic search to find relevant opportunities
- **Engagement Tracking**: Save, bookmark, and apply to initiatives
- **Leader Dashboard**: Create and manage initiatives with analytics

## 🏗️ Architecture

### Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite (embedded, no setup needed)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT + Azure AD B2C (ready)
- **Vector Database**: Qdrant (for AI embeddings)
- **API Documentation**: OpenAPI 3.0 / Swagger
- **Deployment**: Python or Docker

### Architecture Pattern

```
┌─────────────────────────────────────────┐
│         FastAPI Application             │
├─────────────────────────────────────────┤
│  API Layer (Routers & Endpoints)        │
│  - Authentication                        │
│  - User Management                       │
│  - Initiative CRUD                       │
│  - Search & Filtering                    │
│  - AI Recommendations                    │
│  - Engagement Tracking                   │
├─────────────────────────────────────────┤
│  Business Logic Layer                    │
│  - Security & Authorization              │
│  - Data Validation (Pydantic)           │
├─────────────────────────────────────────┤
│  Data Layer                              │
│  - SQLAlchemy ORM                        │
│  - PostgreSQL Database                   │
│  - Qdrant Vector DB                      │
└─────────────────────────────────────────┘
```

## 📋 Features

### Phase 1: Core Backend (✅ Complete)

- [x] User authentication and authorization
- [x] User profile management
- [x] Initiative CRUD operations
- [x] Role-based access control (Analyst/Leader/Admin)
- [x] Search and filtering
- [x] Engagement tracking (save, apply, view)
- [x] Basic recommendations
- [x] API documentation (Swagger)

### Phase 2: AI Enhancement (🚧 In Progress)

- [ ] Vector embeddings generation
- [ ] Semantic search with Qdrant
- [ ] Advanced recommendation algorithm
- [ ] Collaborative filtering
- [ ] Auto-tagging with NLP

### Phase 3: Production Ready (📅 Planned)

- [ ] Azure AD B2C integration
- [ ] Rate limiting
- [ ] Caching (Redis)
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] Admin panel

## 🚦 Getting Started

### Prerequisites

- Python 3.11+
- That's it! (SQLite database included)

### Installation

#### Recommended: Direct Python (No Docker Needed!)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

# API will be available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

The server automatically:
- Creates SQLite database
- Sets up all tables
- Loads sample data
- Displays test credentials

#### Optional: Docker (Simplified)

```bash
# Use simplified docker-compose (no PostgreSQL)
docker-compose -f docker-compose-simple.yml up -d
```

### Database

The application uses **SQLite** (embedded database) - no external database server needed!

- Database file: `./deloitte_initiatives.db`
- Automatically created on first run
- Sample data pre-loaded

To reset database:
```bash
rm deloitte_initiatives.db
python run.py
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Sample API Endpoints

#### Authentication
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/register` - Register new user

#### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/{id}` - Get user by ID

#### Initiatives
- `POST /api/v1/initiatives` - Create initiative (Leader only)
- `GET /api/v1/initiatives` - List initiatives (with filters)
- `GET /api/v1/initiatives/{id}` - Get initiative details
- `PUT /api/v1/initiatives/{id}` - Update initiative
- `DELETE /api/v1/initiatives/{id}` - Delete initiative

#### Search
- `GET /api/v1/search?q=AI healthcare` - Search initiatives
- `GET /api/v1/search/semantic?query=...` - Semantic search (AI)

#### Recommendations
- `GET /api/v1/recommendations` - Get personalized recommendations
- `GET /api/v1/recommendations/user/{id}` - Get recommendations for user

#### Engagement
- `POST /api/v1/engagement/save` - Save/bookmark initiative
- `POST /api/v1/engagement/apply` - Apply to initiative
- `GET /api/v1/engagement/saved` - Get saved initiatives
- `GET /api/v1/engagement/applications` - Get my applications

## 🔐 Authentication

### Development Mode

For testing, use email and password authentication:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "analyst@deloitte.com",
    "password": "password123"
  }'
```

Response includes JWT token:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {...}
}
```

Use the token in subsequent requests:
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer eyJ..."
```

### Test Credentials

All test accounts use password: **password123**

- **analyst@deloitte.com** - Analyst role
- **leader@deloitte.com** - Leader role
- **admin@deloitte.com** - Admin role

### Production Mode (Azure AD B2C)

The backend is ready for Azure AD integration:

1. Configure Azure AD B2C tenant
2. Update `.env` with Azure credentials
3. Use `/api/v1/auth/azure-login` endpoint

## 🗄️ Database Schema

### Core Tables

- **users**: User profiles with skills, interests, and preferences
- **initiatives**: Initiative listings with details and requirements
- **saved_initiatives**: Bookmarked initiatives by users
- **initiative_applications**: User applications to initiatives
- **initiative_views**: View tracking for analytics

### User Roles

- **Analyst**: Browse, search, save, and apply to initiatives
- **Leader**: All analyst permissions + create/manage initiatives
- **Admin**: All permissions + system administration

## 🧪 Sample Data

The system includes sample data for testing:

**Users:** (All passwords: **password123**)
- `analyst@deloitte.com` / password123 (Role: Analyst)
- `leader@deloitte.com` / password123 (Role: Leader)
- `admin@deloitte.com` / password123 (Role: Admin)

**Initiatives:**
- AI Healthcare Research Pod
- Innovation Hub - GenAI Applications
- Financial Services Digital Transformation
- Sustainability Volunteering - Pro Bono

## 🔧 Configuration

Edit `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/deloitte_initiatives

# Authentication
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Azure AD (for production)
AZURE_AD_TENANT_ID=...
AZURE_AD_CLIENT_ID=...
AZURE_AD_CLIENT_SECRET=...

# Vector Database
QDRANT_URL=http://localhost:6333
```

## 🚀 Deployment

### Azure App Service

```bash
# Deploy to Azure
az webapp up --name deloitte-initiatives-api \
  --runtime "PYTHON:3.11" \
  --sku B1

# Configure environment variables
az webapp config appsettings set \
  --name deloitte-initiatives-api \
  --settings DATABASE_URL="..." SECRET_KEY="..."
```

### Docker Deployment

```bash
# Build image
docker build -t deloitte-initiatives-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="..." \
  deloitte-initiatives-api
```

## 📊 API Usage Examples

### Example 1: Search for AI Healthcare Initiatives

```bash
curl "http://localhost:8000/api/v1/search?q=AI%20healthcare&practice_area=Technology"
```

### Example 2: Get Personalized Recommendations

```bash
curl "http://localhost:8000/api/v1/recommendations" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Example 3: Apply to an Initiative

```bash
curl -X POST "http://localhost:8000/api/v1/engagement/apply" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "initiative_id": 1,
    "message": "I am interested in this opportunity because..."
  }'
```

## 📖 Documentation

- **Technical Architecture**: See `ARCHITECTURE.md` for detailed system design
- **API Documentation**: Visit `/docs` endpoint when server is running
- **ER Diagram**: Included in architecture document

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

Proprietary - Deloitte Internal Use Only

## 📞 Support

For questions or issues, contact the development team.

---

**Built with ❤️ for Deloitte Analysts**
