# Technical Architecture Document

## Deloitte Initiative Discovery Platform - Backend

**Version:** 1.0.0  
**Last Updated:** December 2, 2025  
**Author:** Backend Development Team

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Patterns](#architecture-patterns)
3. [Technology Stack](#technology-stack)
4. [Database Design](#database-design)
5. [API Design](#api-design)
6. [Security Architecture](#security-architecture)
7. [AI/ML Components](#aiml-components)
8. [Deployment Architecture](#deployment-architecture)
9. [Scalability & Performance](#scalability--performance)
10. [Future Enhancements](#future-enhancements)

---

## 1. System Overview

### Purpose

The Deloitte Initiative Discovery Platform is designed to solve the problem of fragmented information about firm initiatives. It provides a centralized, intelligent platform for initiative discovery and engagement.

### Key Stakeholders

- **Analysts**: Discover and engage with initiatives
- **Leaders**: Create and manage initiatives
- **Administrators**: System management and oversight

### System Goals

- Centralize initiative information
- Provide AI-powered recommendations
- Enable semantic search capabilities
- Track engagement and analytics
- Facilitate analyst-leader connections

---

## 2. Architecture Patterns

### Layered Architecture

```
┌──────────────────────────────────────────────┐
│         Presentation Layer (API)              │
│  - REST API Endpoints                         │
│  - Request/Response Serialization             │
│  - OpenAPI Documentation                      │
├──────────────────────────────────────────────┤
│         Application Layer                     │
│  - Business Logic                             │
│  - Authentication & Authorization             │
│  - Data Validation                            │
├──────────────────────────────────────────────┤
│         Domain Layer                          │
│  - Domain Models (SQLAlchemy)                 │
│  - Business Entities                          │
│  - Domain Rules                               │
├──────────────────────────────────────────────┤
│         Infrastructure Layer                  │
│  - Database Access (PostgreSQL)               │
│  - Vector Store (Qdrant)                      │
│  - External Services (Azure AD)               │
└──────────────────────────────────────────────┘
```

### Design Principles

1. **Separation of Concerns**: Each layer has distinct responsibilities
2. **Dependency Injection**: FastAPI's dependency system for loose coupling
3. **SOLID Principles**: Especially Single Responsibility and Interface Segregation
4. **DRY (Don't Repeat Yourself)**: Reusable components and utilities
5. **API-First Design**: OpenAPI specification as contract

---

## 3. Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|----------|
| Framework | FastAPI | 0.109.0 | Web framework |
| Language | Python | 3.11+ | Primary language |
| Database | PostgreSQL | 15 | Relational data |
| ORM | SQLAlchemy | 2.0.25 | Database abstraction |
| Vector DB | Qdrant | Latest | Embeddings storage |
| Auth | JWT + Azure AD | - | Authentication |
| API Docs | OpenAPI 3.0 | - | Documentation |
| Containerization | Docker | Latest | Deployment |

### Key Libraries

```python
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9

# Authentication
python-jose[cryptography]==3.3.0
msal==1.26.0

# AI/ML
sentence-transformers==2.3.1
qdrant-client==1.7.3
```

---

## 4. Database Design

### Entity-Relationship Diagram

```
┌─────────────────┐
│     Users       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ full_name       │
│ role            │
│ practice        │
│ skills[]        │
│ interests[]     │
│ industries[]    │
│ ...             │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────┴────────┐       N   ┌─────────────────────┐
│   Initiatives   │◄──────────┤ SavedInitiatives    │
├─────────────────┤           ├─────────────────────┤
│ id (PK)         │           │ id (PK)             │
│ title           │           │ user_id (FK)        │
│ description     │           │ initiative_id (FK)  │
│ practice_area   │           │ saved_at            │
│ skills_needed[] │           └─────────────────────┘
│ industries[]    │
│ tags[]          │           ┌─────────────────────┐
│ status          │      N    │ InitiativeApps      │
│ owner_id (FK)   │◄──────────┤─────────────────────┤
│ ...             │           │ id (PK)             │
└─────────────────┘           │ user_id (FK)        │
                               │ initiative_id (FK)  │
                               │ message             │
                               │ status              │
                               └─────────────────────┘
```

### Table Schemas

#### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    azure_id VARCHAR UNIQUE,
    full_name VARCHAR NOT NULL,
    role VARCHAR NOT NULL,  -- analyst, leader, admin
    bio TEXT,
    practice VARCHAR,
    skills TEXT[],
    interests TEXT[],
    industries TEXT[],
    experience_years INTEGER,
    certifications TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

#### Initiatives Table

```sql
CREATE TABLE initiatives (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    practice_area VARCHAR,
    skills_needed TEXT[],
    industries TEXT[],
    tags TEXT[],
    time_commitment VARCHAR,
    duration VARCHAR,  -- short_term, ongoing, fixed_duration
    duration_details VARCHAR,
    role_type VARCHAR,
    contact_person VARCHAR,
    contact_email VARCHAR,
    status VARCHAR NOT NULL DEFAULT 'open',  -- open, active, full, closed
    owner_id INTEGER REFERENCES users(id),
    view_count INTEGER DEFAULT 0,
    save_count INTEGER DEFAULT 0,
    application_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Indexes

```sql
-- Performance indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_initiatives_owner ON initiatives(owner_id);
CREATE INDEX idx_initiatives_status ON initiatives(status);
CREATE INDEX idx_initiatives_practice ON initiatives(practice_area);
CREATE INDEX idx_saved_user ON saved_initiatives(user_id);
CREATE INDEX idx_saved_initiative ON saved_initiatives(initiative_id);
```

---

## 5. API Design

### REST Principles

- **Resources**: Nouns (users, initiatives, recommendations)
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes**: Appropriate HTTP status codes
- **Pagination**: Query parameters for skip/limit
- **Filtering**: Query parameters for filters

### API Structure

```
/api/v1
├── /auth
│   ├── POST /login
│   ├── POST /register
│   └── POST /azure-login
├── /users
│   ├── GET /me
│   ├── PUT /me
│   ├── GET /{id}
│   └── GET /
├── /initiatives
│   ├── POST /
│   ├── GET /
│   ├── GET /{id}
│   ├── PUT /{id}
│   ├── DELETE /{id}
│   └── GET /my/initiatives
├── /search
│   ├── GET /
│   └── GET /semantic
├── /recommendations
│   ├── GET /
│   └── GET /user/{id}
└── /engagement
    ├── POST /save
    ├── DELETE /save/{id}
    ├── GET /saved
    ├── POST /apply
    ├── GET /applications
    └── GET /initiative/{id}/applications
```

### Request/Response Format

All API requests and responses use JSON format.

**Example Request:**
```json
POST /api/v1/initiatives
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "AI Research Pod",
  "description": "Join our AI research team...",
  "practice_area": "Technology",
  "skills_needed": ["Python", "ML"],
  "time_commitment": "10 hours/week"
}
```

**Example Response:**
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "title": "AI Research Pod",
  "description": "Join our AI research team...",
  "status": "open",
  "owner_id": 2,
  "created_at": "2025-12-02T10:00:00Z",
  ...
}
```

---

## 6. Security Architecture

### Authentication Flow

```
┌──────────┐                  ┌──────────┐                  ┌──────────┐
│  Client  │                  │   API    │                  │ Database │
└────┬─────┘                  └────┬─────┘                  └────┬─────┘
     │                             │                             │
     │ 1. POST /auth/login         │                             │
     │────────────────────────────>│                             │
     │                             │                             │
     │                             │ 2. Validate credentials     │
     │                             │────────────────────────────>│
     │                             │                             │
     │                             │ 3. Return user              │
     │                             │<────────────────────────────│
     │                             │                             │
     │ 4. JWT Token + User         │                             │
     │<────────────────────────────│                             │
     │                             │                             │
     │ 5. GET /users/me            │                             │
     │    Authorization: Bearer... │                             │
     │────────────────────────────>│                             │
     │                             │                             │
     │                             │ 6. Verify JWT               │
     │                             │                             │
     │                             │ 7. Get user                 │
     │                             │────────────────────────────>│
     │                             │                             │
     │ 8. User data                │                             │
     │<────────────────────────────│                             │
```

### Security Measures

1. **JWT Tokens**: Stateless authentication
2. **Password Hashing**: bcrypt for password storage
3. **Role-Based Access Control (RBAC)**: Analyst/Leader/Admin roles
4. **HTTPS**: TLS/SSL in production
5. **CORS**: Configured for allowed origins
6. **Input Validation**: Pydantic schemas
7. **SQL Injection Prevention**: SQLAlchemy parameterized queries
8. **Rate Limiting**: (Planned) Request throttling

### Azure AD B2C Integration (Production)

```python
# Planned implementation
1. User logs in via Azure AD B2C
2. Backend receives Azure AD token
3. Validate token using MSAL
4. Extract user claims (email, groups)
5. Map Azure AD groups to roles
6. Create/update user in database
7. Issue JWT for API access
```

---

## 7. AI/ML Components

### Recommendation System Architecture

```
┌─────────────────────────────────────────────────────┐
│           Recommendation Engine                      │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌────────────────┐      ┌────────────────┐        │
│  │ Content-Based  │      │ Collaborative  │        │
│  │   Filtering    │      │   Filtering    │        │
│  └───────┬────────┘      └────────┬───────┘        │
│          │                        │                  │
│          └────────┬───────────────┘                  │
│                   │                                  │
│          ┌────────┴────────┐                        │
│          │  Hybrid Scoring  │                        │
│          └────────┬────────┘                        │
│                   │                                  │
│          ┌────────┴────────┐                        │
│          │  Ranked Results  │                        │
│          └─────────────────┘                        │
└─────────────────────────────────────────────────────┘
```

### Embedding Pipeline

```
Initiative Text
       │
       ▼
┌──────────────────┐
│  Text Preprocessing│
│  - Lowercase      │
│  - Remove stopwords│
│  - Tokenization   │
└────────┬──────────┘
         │
         ▼
┌──────────────────┐
│  Sentence        │
│  Transformer     │
│  (all-MiniLM)    │
└────────┬──────────┘
         │
         ▼
┌──────────────────┐
│  384-dim Vector  │
│  Embedding       │
└────────┬──────────┘
         │
         ▼
┌──────────────────┐
│  Store in Qdrant │
│  Vector DB       │
└──────────────────┘
```

### Semantic Search Flow

```python
# 1. Generate embedding for query
query = "AI healthcare initiatives"
query_embedding = model.encode(query)

# 2. Search vector database
results = qdrant_client.search(
    collection_name="initiatives",
    query_vector=query_embedding,
    limit=10
)

# 3. Retrieve full initiative data
initiative_ids = [r.id for r in results]
initiatives = db.query(Initiative).filter(
    Initiative.id.in_(initiative_ids)
).all()

# 4. Return ranked results with scores
```

### Recommendation Scoring

```python
score = (
    0.4 * skill_match_score +      # Skill overlap
    0.3 * semantic_similarity +     # Embedding similarity
    0.2 * interaction_score +       # Past interactions
    0.1 * popularity_score          # Initiative popularity
)
```

---

## 8. Deployment Architecture

### Docker Containers

```
┌─────────────────────────────────────────────────┐
│              Docker Compose Stack               │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐  ┌──────────────┐           │
│  │   FastAPI    │  │  PostgreSQL  │           │
│  │  Container   │  │  Container   │           │
│  │  Port: 8000  │  │  Port: 5432  │           │
│  └──────┬───────┘  └──────┬───────┘           │
│         │                 │                     │
│         │                 │                     │
│  ┌──────┴─────────────────┴───────┐           │
│  │         Network Bridge          │           │
│  └──────┬─────────────────────────┘           │
│         │                                       │
│  ┌──────┴───────┐                              │
│  │   Qdrant     │                              │
│  │  Container   │                              │
│  │  Port: 6333  │                              │
│  └──────────────┘                              │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Azure Deployment

```
┌─────────────────────────────────────────────────┐
│              Azure Cloud                         │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │      Azure App Service (Linux)         │    │
│  │      - FastAPI Application             │    │
│  │      - Auto-scaling enabled            │    │
│  └────────────┬───────────────────────────┘    │
│               │                                 │
│  ┌────────────┴───────────────────────────┐    │
│  │   Azure Database for PostgreSQL        │    │
│  │   - Managed service                     │    │
│  │   - Automated backups                   │    │
│  └────────────┬───────────────────────────┘    │
│               │                                 │
│  ┌────────────┴───────────────────────────┐    │
│  │   Azure AD B2C                          │    │
│  │   - Authentication                      │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │   Qdrant Cloud / Azure Container       │    │
│  │   - Vector database                     │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 9. Scalability & Performance

### Performance Optimizations

1. **Database Indexing**: Indexes on frequently queried columns
2. **Connection Pooling**: SQLAlchemy connection pool
3. **Lazy Loading**: Load relationships only when needed
4. **Pagination**: Limit result sets
5. **Caching**: Redis for frequently accessed data (planned)
6. **Vector Search**: Fast approximate nearest neighbor search

### Scalability Strategies

1. **Horizontal Scaling**: Multiple API instances behind load balancer
2. **Database Replication**: Read replicas for read-heavy operations
3. **Async Operations**: Background tasks for heavy computations
4. **CDN**: Static content delivery
5. **Microservices**: Future split into specialized services

### Load Handling

- **Current Capacity**: ~100 requests/second (single instance)
- **Scaled Capacity**: ~1000 requests/second (10 instances)
- **Database**: PostgreSQL can handle 10,000+ connections with proper tuning

---

## 10. Future Enhancements

### Phase 2: Enhanced AI

- [ ] Full vector search implementation
- [ ] Collaborative filtering
- [ ] Learning from user interactions
- [ ] Auto-tagging with NLP
- [ ] Skill extraction from profiles

### Phase 3: Advanced Features

- [ ] Real-time notifications (WebSockets)
- [ ] Email notifications
- [ ] Analytics dashboard
- [ ] Admin panel
- [ ] Reporting system
- [ ] API rate limiting
- [ ] Redis caching
- [ ] GraphQL API option

### Phase 4: Enterprise

- [ ] Multi-tenancy support
- [ ] Advanced RBAC
- [ ] Audit logging
- [ ] Data export/import
- [ ] Integration with Workday
- [ ] Integration with SharePoint
- [ ] Mobile app backend support

---

## Appendix

### Performance Benchmarks

| Endpoint | Avg Response Time | Throughput |
|----------|------------------|------------|
| GET /initiatives | 50ms | 200 req/s |
| POST /initiatives | 100ms | 100 req/s |
| GET /search | 75ms | 150 req/s |
| GET /recommendations | 200ms | 50 req/s |

### Error Handling

All API errors follow this format:

```json
{
  "detail": "Error message description",
  "status_code": 400
}
```

Common status codes:
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

---

**Document Version:** 1.0.0  
**Last Review:** December 2, 2025  
**Next Review:** March 2, 2026