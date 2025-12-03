# API Documentation

## Deloitte Initiative Discovery Platform API

**Base URL**: `http://localhost:8000/api/v1`  
**Version**: 1.0.0  
**Authentication**: Bearer JWT Token

---

## Overview

This API provides a complete backend for the Deloitte Initiative Discovery Platform, enabling analysts to discover firm initiatives and leaders to manage initiative listings.

### Quick Links

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Login

**POST** `/api/v1/auth/login`

Login with email to receive JWT token.

**Request Body:**
```json
{
  "email": "analyst@deloitte.com"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "analyst@deloitte.com",
    "full_name": "John Analyst",
    "role": "analyst",
    "practice": "Strategy",
    "skills": ["Python", "Data Analysis"],
    "interests": ["AI", "Healthcare"],
    "created_at": "2025-12-02T10:00:00Z"
  }
}
```

### Register

**POST** `/api/v1/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "newuser@deloitte.com",
  "full_name": "New User",
  "role": "analyst"
}
```

---

## User Management

### Get Current User Profile

**GET** `/api/v1/users/me`

Get the authenticated user's profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "analyst@deloitte.com",
  "full_name": "John Analyst",
  "role": "analyst",
  "bio": "Strategy consultant with 3 years experience",
  "practice": "Strategy",
  "skills": ["Python", "Data Analysis", "PowerBI"],
  "interests": ["AI", "Healthcare"],
  "industries": ["Healthcare", "Financial Services"],
  "experience_years": 3,
  "certifications": ["PMP"],
  "created_at": "2025-12-02T10:00:00Z",
  "updated_at": "2025-12-02T10:00:00Z"
}
```

### Update User Profile

**PUT** `/api/v1/users/me`

Update the authenticated user's profile.

**Request Body:**
```json
{
  "bio": "Updated bio",
  "skills": ["Python", "Machine Learning", "Data Science"],
  "interests": ["AI", "Healthcare", "Innovation"],
  "industries": ["Healthcare"],
  "experience_years": 4
}
```

### Get User by ID

**GET** `/api/v1/users/{user_id}`

Get any user's profile by ID.

---

## Initiative Management

### Create Initiative

**POST** `/api/v1/initiatives/`

Create a new initiative (Leader role required).

**Request Body:**
```json
{
  "title": "AI Healthcare Research Pod",
  "description": "Join our research team exploring AI in healthcare...",
  "practice_area": "Technology",
  "skills_needed": ["Python", "Machine Learning", "Healthcare Knowledge"],
  "industries": ["Healthcare"],
  "time_commitment": "5-10 hours/week",
  "duration": "ongoing",
  "role_type": "Researcher",
  "contact_person": "Sarah Leader",
  "contact_email": "leader@deloitte.com"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "AI Healthcare Research Pod",
  "description": "Join our research team...",
  "practice_area": "Technology",
  "skills_needed": ["Python", "Machine Learning"],
  "status": "open",
  "owner_id": 2,
  "view_count": 0,
  "save_count": 0,
  "application_count": 0,
  "created_at": "2025-12-02T10:00:00Z"
}
```

### List Initiatives

**GET** `/api/v1/initiatives/?skip=0&limit=20&status=open&practice_area=Technology`

List all initiatives with optional filters.

**Query Parameters:**
- `skip` (int): Number of items to skip (default: 0)
- `limit` (int): Max items to return (default: 20, max: 100)
- `status` (string): Filter by status (open, active, full, closed)
- `practice_area` (string): Filter by practice area

**Response:**
```json
{
  "total": 50,
  "items": [
    {
      "id": 1,
      "title": "AI Healthcare Research Pod",
      "description": "...",
      "status": "open"
    }
  ],
  "page": 1,
  "page_size": 20
}
```

### Get Initiative

**GET** `/api/v1/initiatives/{initiative_id}`

Get details of a specific initiative.

### Update Initiative

**PUT** `/api/v1/initiatives/{initiative_id}`

Update an initiative (owner or admin only).

**Request Body:**
```json
{
  "status": "full",
  "description": "Updated description"
}
```

### Delete Initiative

**DELETE** `/api/v1/initiatives/{initiative_id}`

Delete an initiative (owner or admin only).

### Get My Initiatives

**GET** `/api/v1/initiatives/my/initiatives`

Get all initiatives created by the authenticated user.

---

## Search & Discovery

### Search Initiatives

**GET** `/api/v1/search/?q=AI%20healthcare&skills=Python&practice_area=Technology`

Search and filter initiatives.

**Query Parameters:**
- `q` (string): Search query (searches title and description)
- `skills` (list[string]): Filter by required skills
- `practice_area` (string): Filter by practice area
- `industries` (list[string]): Filter by industries
- `time_commitment` (string): Filter by time commitment
- `skip` (int): Pagination offset
- `limit` (int): Results per page

**Examples:**

```bash
# Search for AI healthcare initiatives
GET /api/v1/search?q=AI%20healthcare

# Find Python opportunities in Technology practice
GET /api/v1/search?skills=Python&practice_area=Technology

# Combine filters
GET /api/v1/search?q=innovation&skills=GenAI&practice_area=Technology&limit=10
```

### Semantic Search (AI-Powered)

**GET** `/api/v1/search/semantic?query=Find%20volunteering%20opportunities&limit=10`

Natural language semantic search powered by AI embeddings.

**Query Parameters:**
- `query` (string, required): Natural language search query
- `limit` (int): Max results (default: 10, max: 50)

**Examples:**

```bash
# Natural language queries
GET /api/v1/search/semantic?query=Find initiatives involving AI and healthcare

GET /api/v1/search/semantic?query=Short-term volunteering projects

GET /api/v1/search/semantic?query=Innovation opportunities in financial services
```

---

## AI Recommendations

### Get Personalized Recommendations

**GET** `/api/v1/recommendations/?limit=10`

Get AI-powered personalized recommendations based on your profile.

**Response:**
```json
[
  {
    "initiative": {
      "id": 1,
      "title": "AI Healthcare Research Pod",
      "description": "...",
      "skills_needed": ["Python", "Machine Learning"],
      "status": "open"
    },
    "score": 0.85,
    "explanation": "Matched skills: Python, Machine Learning; Same practice area: Technology"
  }
]
```

### Get Recommendations for User

**GET** `/api/v1/recommendations/user/{user_id}?limit=10`

Get recommendations for a specific user (useful for leaders).

---

## Engagement

### Save Initiative

**POST** `/api/v1/engagement/save`

Bookmark an initiative for later.

**Request Body:**
```json
{
  "initiative_id": 1
}
```

### Remove Saved Initiative

**DELETE** `/api/v1/engagement/save/{initiative_id}`

Remove an initiative from bookmarks.

### Get Saved Initiatives

**GET** `/api/v1/engagement/saved`

Get all saved/bookmarked initiatives.

**Response:**
```json
[
  {
    "id": 1,
    "title": "AI Healthcare Research Pod",
    "description": "...",
    "status": "open"
  }
]
```

### Apply to Initiative

**POST** `/api/v1/engagement/apply`

Express interest or apply to an initiative.

**Request Body:**
```json
{
  "initiative_id": 1,
  "message": "I'm very interested in this opportunity because..."
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "initiative_id": 1,
  "message": "I'm very interested...",
  "applied_at": "2025-12-02T10:00:00Z",
  "status": "pending"
}
```

### Get My Applications

**GET** `/api/v1/engagement/applications`

Get all applications submitted by the authenticated user.

### Get Initiative Applications

**GET** `/api/v1/engagement/initiative/{initiative_id}/applications`

Get all applications for a specific initiative (owner/admin only).

---

## Data Models

### User

```typescript
{
  id: number
  email: string
  full_name: string
  role: "analyst" | "leader" | "admin"
  bio?: string
  practice?: string
  skills: string[]
  interests: string[]
  industries: string[]
  experience_years?: number
  certifications: string[]
  created_at: datetime
  updated_at: datetime
}
```

### Initiative

```typescript
{
  id: number
  title: string
  description: string
  practice_area?: string
  skills_needed: string[]
  industries: string[]
  tags: string[]
  time_commitment?: string
  duration: "short_term" | "ongoing" | "fixed_duration"
  duration_details?: string
  role_type?: string
  contact_person?: string
  contact_email?: string
  status: "open" | "active" | "full" | "closed"
  owner_id: number
  view_count: number
  save_count: number
  application_count: number
  created_at: datetime
  updated_at: datetime
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Successful deletion
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Rate Limiting

*Coming soon*

Rate limiting will be implemented in Phase 3.

---

## Pagination

List endpoints support pagination:

```
GET /api/v1/initiatives?skip=0&limit=20
```

- `skip`: Number of items to skip (default: 0)
- `limit`: Number of items to return (default: 20, max: 100)

Response includes pagination metadata:

```json
{
  "total": 150,
  "items": [...],
  "page": 1,
  "page_size": 20
}
```

---

## Examples

### Complete User Flow

```bash
# 1. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "analyst@deloitte.com"}'

# Save the token
TOKEN="eyJhbGci..."

# 2. Update profile
curl -X PUT "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Python", "Machine Learning"],
    "interests": ["AI", "Healthcare"]
  }'

# 3. Search for initiatives
curl "http://localhost:8000/api/v1/search?q=AI%20healthcare" \
  -H "Authorization: Bearer $TOKEN"

# 4. Get personalized recommendations
curl "http://localhost:8000/api/v1/recommendations" \
  -H "Authorization: Bearer $TOKEN"

# 5. Save an initiative
curl -X POST "http://localhost:8000/api/v1/engagement/save" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"initiative_id": 1}'

# 6. Apply to an initiative
curl -X POST "http://localhost:8000/api/v1/engagement/apply" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "initiative_id": 1,
    "message": "I am very interested in this opportunity!"
  }'
```

---

## Testing

Sample test users are pre-loaded:

- **analyst@deloitte.com** - Analyst role
- **leader@deloitte.com** - Leader role
- **admin@deloitte.com** - Admin role

Sample initiatives are also pre-loaded for testing.

---

## Support

For API issues or questions:
- Check the Swagger UI: http://localhost:8000/docs
- Review the architecture document: `ARCHITECTURE.md`
- Contact the development team

---

**Last Updated**: December 2, 2025  
**API Version**: 1.0.0