# Authentication Guide

## Email & Password Authentication

The Deloitte Initiative Discovery Platform uses **JWT (JSON Web Token)** authentication with email and password credentials.

---

## 🔐 How It Works

1. **User logs in** with email and password
2. **Server validates** credentials against database
3. **JWT token issued** (valid for 30 minutes)
4. **Client includes token** in subsequent requests
5. **Server validates token** on each request

---

## 📧 Test Accounts

Pre-configured test accounts with default password:

| Email | Password | Role | Description |
|-------|----------|------|-------------|
| analyst@deloitte.com | password123 | Analyst | Browse, search, apply to initiatives |
| leader@deloitte.com | password123 | Leader | Create and manage initiatives |
| admin@deloitte.com | password123 | Admin | Full system access |

---

## 🚀 Quick Start

### 1. Start the Server

```bash
# Using Docker
docker-compose up -d

# OR using Python
python run.py
```

### 2. Login via Swagger UI

1. Open: http://localhost:8000/docs
2. Find **POST /api/v1/auth/login**
3. Click "Try it out"
4. Enter credentials:
   ```json
   {
     "email": "analyst@deloitte.com",
     "password": "password123"
   }
   ```
5. Click "Execute"
6. Copy the `access_token` from response

### 3. Authorize

1. Click the 🔒 **"Authorize"** button at top of Swagger UI
2. Enter: `Bearer <paste-your-token>`
3. Click "Authorize"
4. Now you can access protected endpoints!

---

## 🔧 API Endpoints

### Login

**POST** `/api/v1/auth/login`

Authenticate with email and password to receive JWT token.

**Request:**
```json
{
  "email": "analyst@deloitte.com",
  "password": "password123"
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

**Request:**
```json
{
  "email": "newuser@deloitte.com",
  "password": "securepassword",
  "full_name": "New User",
  "role": "analyst"
}
```

---

## 💻 Using the API

### cURL Examples

#### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "analyst@deloitte.com",
    "password": "password123"
  }'
```

#### Use Token
```bash
# Save token
TOKEN="eyJhbGci..."

# Get current user
curl "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer $TOKEN"

# Get recommendations
curl "http://localhost:8000/api/v1/recommendations" \
  -H "Authorization: Bearer $TOKEN"

# Search initiatives
curl "http://localhost:8000/api/v1/search?q=AI" \
  -H "Authorization: Bearer $TOKEN"
```

### Python Example

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "email": "analyst@deloitte.com",
        "password": "password123"
    }
)

data = response.json()
token = data["access_token"]
user = data["user"]

print(f"Logged in as: {user['full_name']}")
print(f"Token: {token[:50]}...")

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}

# Get profile
profile = requests.get(
    "http://localhost:8000/api/v1/users/me",
    headers=headers
).json()
print(f"Profile: {profile}")

# Get recommendations
recommendations = requests.get(
    "http://localhost:8000/api/v1/recommendations",
    headers=headers
).json()
print(f"Got {len(recommendations)} recommendations")
```

### JavaScript Example

```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'analyst@deloitte.com',
    password: 'password123'
  })
});

const { access_token, user } = await loginResponse.json();
console.log(`Logged in as: ${user.full_name}`);

// Use token
const profileResponse = await fetch('http://localhost:8000/api/v1/users/me', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});

const profile = await profileResponse.json();
console.log('Profile:', profile);
```

---

## 🔒 Security Features

### Password Security
- ✅ **Bcrypt hashing** with automatic salt generation
- ✅ **Minimum 6 characters** required
- ✅ **Never stored in plaintext**
- ✅ **Secure comparison** (timing attack resistant)

### Token Security
- ✅ **JWT tokens** with HS256 algorithm
- ✅ **30-minute expiration** (configurable)
- ✅ **Signed with secret key**
- ✅ **Includes user ID and email**
- ✅ **Stateless** (no server-side sessions)

### API Security
- ✅ **Bearer token authentication**
- ✅ **Role-based access control**
- ✅ **Input validation** (Pydantic)
- ✅ **SQL injection prevention** (SQLAlchemy)
- ✅ **CORS configuration**

---

## ⚙️ Configuration

### Environment Variables

In `.env` file:

```env
# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/deloitte_initiatives
```

### Generate Strong Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🔄 Token Lifecycle

```
1. User submits email + password
         ↓
2. Server validates credentials
         ↓
3. Server generates JWT token
   - Payload: { sub: email, user_id: id, exp: timestamp }
   - Signed with SECRET_KEY
         ↓
4. Client receives token
         ↓
5. Client includes token in Authorization header
   - Format: "Bearer <token>"
         ↓
6. Server validates token
   - Verifies signature
   - Checks expiration
   - Extracts user info
         ↓
7. Request processed with user context
```

---

## 🚨 Error Handling

### 401 Unauthorized

**Cause:** Invalid credentials or expired token

```json
{
  "detail": "Incorrect email or password"
}
```

**Solution:**
- Check email and password
- Login again to get new token

### 403 Forbidden

**Cause:** Insufficient permissions

```json
{
  "detail": "Not enough permissions. Leader role required."
}
```

**Solution:**
- Use account with appropriate role
- Contact admin for role upgrade

### 422 Validation Error

**Cause:** Invalid request format

```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Solution:**
- Check request body format
- Ensure all required fields present

---

## 🎯 Role-Based Permissions

### Analyst Role
- ✅ View initiatives
- ✅ Search and filter
- ✅ Save/bookmark initiatives
- ✅ Apply to initiatives
- ✅ Get recommendations
- ✅ Update own profile
- ❌ Create initiatives
- ❌ Manage others' initiatives

### Leader Role
- ✅ All Analyst permissions
- ✅ Create initiatives
- ✅ Update own initiatives
- ✅ Delete own initiatives
- ✅ View applications to own initiatives
- ❌ Delete others' initiatives

### Admin Role
- ✅ All Leader permissions
- ✅ Update any initiative
- ✅ Delete any initiative
- ✅ View all applications
- ✅ Manage users

---

## 🧪 Testing Authentication

Run the test script:

```bash
python test_auth.py
```

Expected output:
```
============================================================
Testing Password Authentication
============================================================

1. Original password: password123
2. Hashed password: $2b$12$...
3. Verify correct password: True
4. Verify incorrect password: False

✅ Password hashing and verification working correctly!

============================================================
Testing Database Connection and User Creation
============================================================

✅ Database connection successful!
   Current users in database: 3

   Sample user:
   - Email: analyst@deloitte.com
   - Name: John Analyst
   - Role: analyst
   - Has password hash: True
   - Password 'password123' valid: True

============================================================
✅ All authentication tests passed!
============================================================
```

---

## 📝 Creating New Users

### Via API

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newanalyst@deloitte.com",
    "password": "securepass123",
    "full_name": "Jane Analyst",
    "role": "analyst"
  }'
```

### Via Python Script

```python
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole

db = SessionLocal()

# Create new user
new_user = User(
    email="newuser@deloitte.com",
    password_hash=get_password_hash("password123"),
    full_name="New User",
    role=UserRole.ANALYST
)

db.add(new_user)
db.commit()
print(f"Created user: {new_user.email}")
```

---

## 🔐 Best Practices

### For Development
1. ✅ Use test accounts provided
2. ✅ Store tokens securely in memory
3. ✅ Don't commit passwords to git
4. ✅ Use environment variables for secrets

### For Production
1. ✅ Use strong secret keys (32+ bytes)
2. ✅ Enable HTTPS/SSL
3. ✅ Implement rate limiting
4. ✅ Add refresh token support
5. ✅ Enable password reset flow
6. ✅ Implement account lockout
7. ✅ Add audit logging
8. ✅ Use Azure AD B2C (future)

---

## 🆘 Troubleshooting

### Login returns 500 error

**Cause:** Database not initialized or connection issue

**Solution:**
```bash
# Initialize database
python -c "from app.core.init_db import init_db, seed_sample_data; init_db(); seed_sample_data()"

# Or restart with Docker
docker-compose down -v
docker-compose up -d
```

### Invalid credentials error

**Cause:** Wrong email or password

**Solution:**
- Use test accounts: analyst@deloitte.com / password123
- Check for typos
- Ensure account exists in database

### Token expired error

**Cause:** Token older than 30 minutes

**Solution:**
- Login again to get new token
- Tokens expire for security

---

## 📚 Related Documentation

- **API Documentation**: See `API_DOCUMENTATION.md`
- **Quick Start**: See `QUICKSTART.md`
- **Deployment**: See `DEPLOYMENT_GUIDE.md`

---

**Last Updated**: December 2, 2025  
**Auth Version**: JWT with bcrypt password hashing
